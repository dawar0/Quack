from flask import Blueprint, request, current_app, send_file
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.orm import joinedload
from ..models import Service, ServiceRequest, User, Document
from ..database import db
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from .service import service_model
from .auth import customer_required
from ..utils.cache import cache_result, delete_pattern
from ..tasks.email_tasks import send_notification_email_task
import os
from datetime import datetime

customer_bp = Namespace("customer", description="Customer operations")

user_details_model = customer_bp.model(
    "UserDetails",
    {
        "id": fields.Integer(readonly=True),
        "username": fields.String(required=True),
        "name": fields.String(),
        "email": fields.String(),
        "phone_number": fields.String(),
        "address": fields.String(),
        "profile_image": fields.String(),
        "date_created": fields.DateTime(attribute="created_at"),
        "blocked": fields.Boolean(),
    },
    model_id="customer_user_details_model",
)

service_request_creation_model = customer_bp.model(
    "ServiceRequestCreation",
    {
        "service_id": fields.Integer(
            required=True, description="The ID of the requested service"
        ),
        "preferred_date": fields.Date(description="Preferred date for the service"),
        "location_pin_code": fields.String(description="Pin code of the location"),
        "remarks": fields.String(description="Any additional remarks"),
    },
    model_id="customer_service_request_creation_model",
)

service_request_model = customer_bp.model(
    "ServiceRequest",
    {
        "id": fields.Integer(readonly=True),
        "service_id": fields.Integer(required=True),
        "customer_id": fields.Integer(required=True),
        "professional_id": fields.Integer(),
        "date_of_request": fields.DateTime(),
        "date_of_completion": fields.DateTime(),
        "service_status": fields.String(),
        "remarks": fields.String(),
        "location_pin_code": fields.String(),
        "preferred_date": fields.Date(),
        "user": fields.Nested(user_details_model),
        "service": fields.Nested(service_model),
        "professional": fields.Nested(user_details_model),
        "customer": fields.Nested(user_details_model),
    },
    model_id="customer_service_request_model",
)

action_on_request_model = customer_bp.model(
    "ActionOnRequest",
    {
        "request_id": fields.Integer(
            required=True, description="ID of the service request"
        ),
        "action": fields.String(
            required=True,
            enum=["cancel"],
            description="Action to take on the request",
        ),
    },
    model_id="customer_action_on_request_model",
)

action_response_model = customer_bp.model(
    "ActionResponse",
    {"message": fields.String(description="Response message")},
    model_id="customer_action_response_model",
)


@customer_bp.route("/requests")
class CustomerRequests(Resource):
    @jwt_required()
    @customer_bp.expect(service_request_creation_model)
    @customer_bp.marshal_with(service_request_model, code=201)
    def post(self):
        """Create a new service request."""
        data = request.get_json()
        service_id = data.get("service_id")
        preferred_date = data.get("preferred_date")
        location_pin_code = data.get("location_pin_code")
        remarks = data.get("remarks")
        customer_id = get_jwt_identity()

        # Convert preferred_date string to Python date object
        if preferred_date and isinstance(preferred_date, str):
            preferred_date = datetime.strptime(preferred_date, "%Y-%m-%d").date()

        service = Service.query.get_or_404(service_id)
        new_request = ServiceRequest(
            service_id=service_id,
            customer_id=customer_id,
            preferred_date=preferred_date,
            location_pin_code=location_pin_code,
            remarks=remarks,
        )
        db.session.add(new_request)
        db.session.commit()

        delete_pattern(f"customer:requests:{customer_id}")
        delete_pattern(f"customer:stats:{customer_id}")
        delete_pattern(f"customer:activity:{customer_id}")

        # Send confirmation email to the customer
        customer = User.query.get(customer_id)
        if customer and customer.email:
            service_name = service.name if service else "service"
            send_notification_email_task.delay(
                subject=f"Service Request Confirmation - #{new_request.id}",
                user_email=customer.email,
                user_name=customer.name or customer.username,
                message=f"Your request for {service_name} has been submitted successfully. "
                f"Request ID: #{new_request.id}. We will notify you when a professional accepts your request.",
            )

        return new_request, 201

    @jwt_required()
    @customer_bp.marshal_list_with(service_request_model)
    @cache_result("customer:requests:{identity}", expiration=300)
    def get(self):
        """List all service requests for the logged-in customer."""
        customer_id = get_jwt_identity()
        return (
            ServiceRequest.query.filter_by(customer_id=customer_id)
            .options(
                joinedload(ServiceRequest.customer),
                joinedload(ServiceRequest.service),
                joinedload(ServiceRequest.professional),
            )
            .all()
        )


@customer_bp.route("/requests/<int:request_id>")
class CustomerRequestDetail(Resource):
    @jwt_required()
    @customer_bp.marshal_with(service_request_model)
    @customer_bp.response(404, "Request not found")
    @cache_result("customer:request:{request_id}:{identity}", expiration=300)
    def get(self, request_id):
        """Get details of a specific service request for the logged-in customer."""
        customer_id = get_jwt_identity()
        request = ServiceRequest.query.filter_by(
            id=request_id, customer_id=customer_id
        ).first_or_404()
        return request


@customer_bp.route("/requests/take_action")
class TakeActionOnRequest(Resource):
    @jwt_required()
    @customer_bp.expect(action_on_request_model, validate=True)
    @customer_bp.doc(description="Cancel a service request.")
    @customer_bp.marshal_with(action_response_model)
    def post(self):
        """Cancel a service request."""
        data = request.get_json()
        request_id = data.get("request_id")
        action = data.get("action").lower()
        customer_id = get_jwt_identity()

        service_request = ServiceRequest.query.filter_by(
            id=request_id, customer_id=customer_id
        ).first_or_404()

        if action == "cancel":
            # Only allow cancellation if the request is not already completed
            if service_request.service_status in ["Completed", "Cancelled"]:
                return (
                    customer_bp.marshal(
                        {
                            "message": "Cannot cancel a completed or already cancelled request"
                        },
                        action_response_model,
                    ),
                    400,
                )

            service_request.service_status = "Cancelled"
            db.session.commit()

            delete_pattern(f"customer:requests:{customer_id}")
            delete_pattern(f"customer:request:{request_id}:{customer_id}")
            delete_pattern(f"customer:stats:{customer_id}")
            delete_pattern(f"customer:activity:{customer_id}")
            delete_pattern(
                "professional:requests"
            )  # Invalidate main professional requests cache
            delete_pattern(
                "professional:requests:available"
            )  # Invalidate available requests cache

            if service_request.professional_id:
                delete_pattern(
                    f"professional:requests:assigned:{service_request.professional_id}"
                )
                delete_pattern(f"professional:request:{request_id}")
                delete_pattern(
                    f"professional:dashboard:stats:{service_request.professional_id}"
                )
                delete_pattern(
                    f"professional:dashboard:activity:{service_request.professional_id}"
                )

                # Notify the professional if one was assigned
                professional = User.query.get(service_request.professional_id)
                if professional and professional.email:
                    service_name = (
                        service_request.service.name
                        if service_request.service
                        else "service"
                    )
                    send_notification_email_task.delay(
                        subject=f"Service Request Cancelled - #{request_id}",
                        user_email=professional.email,
                        user_name=professional.name or professional.username,
                        message=f"The customer has cancelled service request #{request_id} for {service_name}.",
                    )

            # Notify the customer of successful cancellation
            customer = User.query.get(customer_id)
            if customer and customer.email:
                service_name = (
                    service_request.service.name
                    if service_request.service
                    else "service"
                )
                send_notification_email_task.delay(
                    subject=f"Service Request Cancelled - #{request_id}",
                    user_email=customer.email,
                    user_name=customer.name or customer.username,
                    message=f"Your service request #{request_id} for {service_name} has been cancelled successfully.",
                )

            return (
                customer_bp.marshal(
                    {"message": f"Request {request_id} has been cancelled"},
                    action_response_model,
                ),
                200,
            )
        else:
            return (
                customer_bp.marshal(
                    {"message": "Invalid action"}, action_response_model
                ),
                400,
            )


# Activity feed model for the dashboard
activity_item_model = customer_bp.model(
    "ActivityItem",
    {
        "id": fields.String(description="Unique identifier for the activity"),
        "type": fields.String(
            description="Type of activity (e.g., service_request, payment)"
        ),
        "action": fields.String(
            description="Action performed (created, completed, etc.)"
        ),
        "service": fields.String(description="Service name", required=False),
        "amount": fields.Float(
            description="Amount involved (for payments)", required=False
        ),
        "professional": fields.String(description="Professional name", required=False),
        "professional_id": fields.Integer(
            description="Professional ID", required=False
        ),
        "timestamp": fields.DateTime(description="When the activity occurred"),
    },
    model_id="customer_activity_item_model",
)


@customer_bp.route("/dashboard/activity")
class CustomerActivityFeed(Resource):
    @jwt_required()
    @customer_bp.marshal_list_with(activity_item_model)
    @customer_bp.doc(description="Get activity feed for the logged-in customer.")
    @cache_result("customer:activity:{identity}", expiration=300)
    def get(self):
        """Get activity feed for the logged-in customer."""
        from sqlalchemy import desc

        customer_id = get_jwt_identity()

        # Get recent service requests
        service_requests = (
            ServiceRequest.query.filter_by(customer_id=customer_id)
            .join(Service, ServiceRequest.service_id == Service.id)
            .order_by(desc(ServiceRequest.date_of_request))
            .limit(10)
            .all()
        )

        # Format the activity feed
        activity_feed = []
        for req in service_requests:
            # Determine action based on status
            action = ""
            if req.service_status == "Pending":
                action = "created"
            elif req.service_status == "Completed":
                action = "completed"
            elif req.service_status == "Cancelled":
                action = "canceled"
            elif req.service_status == "Accepted":
                action = "accepted"

            activity_feed.append(
                {
                    "id": f"sr-{req.id}",
                    "type": "service_request",
                    "action": action,
                    "service": req.service.name,
                    "professional": req.professional.name if req.professional else None,
                    "professional_id": req.professional_id,
                    "timestamp": req.date_of_request,
                }
            )

            # If completed, add a payment activity
            if req.service_status == "Completed" and req.service.price:
                activity_feed.append(
                    {
                        "id": f"payment-{req.id}",
                        "type": "payment",
                        "action": "paid",
                        "service": req.service.name,
                        "amount": float(req.service.price),
                        "professional": (
                            req.professional.name if req.professional else None
                        ),
                        "professional_id": req.professional_id,
                        "timestamp": req.date_of_completion or req.date_of_request,
                    }
                )

        return activity_feed


@customer_bp.route("/profile")
class CustomerProfile(Resource):
    @customer_bp.marshal_with(user_details_model)
    @customer_bp.doc(description="Get customer profile")
    @customer_required()
    @cache_result("customer:profile:{identity}", expiration=600)
    def get(self):
        """Get customer profile."""
        customer_id = get_jwt_identity()
        return User.query.get_or_404(customer_id)

    @customer_bp.expect(user_details_model)
    @customer_bp.marshal_with(user_details_model)
    @customer_bp.doc(description="Update customer profile")
    @customer_required()
    def put(self):
        """Update customer profile."""
        customer_id = get_jwt_identity()
        customer = User.query.get_or_404(customer_id)
        data = request.get_json()

        # Update allowed fields
        allowed_fields = [
            "name",
            "phone_number",
            "address",
        ]

        for field in allowed_fields:
            if field in data:
                setattr(customer, field, data[field])

        db.session.commit()

        delete_pattern(f"customer:profile:{customer_id}")
        delete_pattern(f"customer:stats:{customer_id}")
        delete_pattern(f"customer:activity:{customer_id}")

        return customer


@customer_bp.route("/password")
class CustomerPassword(Resource):
    @customer_bp.doc(description="Change customer password")
    @customer_required()
    def put(self):
        """Change customer password."""
        data = request.get_json()
        current_password = data.get("current_password")
        new_password = data.get("new_password")

        if not current_password or not new_password:
            return {"message": "Current password and new password are required"}, 400

        customer_id = get_jwt_identity()
        user = User.query.get_or_404(customer_id)

        if not check_password_hash(user.password, current_password):
            return {"message": "Current password is incorrect"}, 401

        user.password = generate_password_hash(new_password)
        db.session.commit()

        # Invalidate relevant caches
        delete_pattern(f"customer:profile:{customer_id}")

        return {"message": "Password updated successfully"}, 200


@customer_bp.route("/profile/picture")
class CustomerProfilePicture(Resource):
    @customer_bp.doc(description="Get customer profile picture")
    @customer_required()
    def get(self):
        """Get customer profile picture."""
        customer_id = get_jwt_identity()
        user = User.query.get_or_404(customer_id)

        if not user.profile_image:
            return {"message": "No profile picture found"}, 404

        # Build the path to the profile image
        file_path = os.path.join(
            current_app.config["UPLOAD_FOLDER"], user.profile_image
        )

        # Check if file exists
        if not os.path.exists(file_path):
            return {"message": "Profile image file not found on server"}, 404

        # Get file extension and set appropriate MIME type
        file_ext = os.path.splitext(user.profile_image)[1].lower()
        mime_types = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".gif": "image/gif",
        }
        mimetype = mime_types.get(file_ext, "application/octet-stream")

        # Return the file
        return send_file(
            file_path,
            mimetype=mimetype,
            download_name=user.profile_image,
            as_attachment=False,
        )

    @customer_bp.doc(description="Update customer profile picture")
    @customer_required()
    def put(self):
        """Update customer profile picture."""
        if "profile_picture" not in request.files:
            return {"message": "No profile picture provided"}, 400

        file = request.files["profile_picture"]
        if file.filename == "":
            return {"message": "No selected file"}, 400

        if file and allowed_file(file.filename):
            customer_id = get_jwt_identity()
            user = User.query.get_or_404(customer_id)

            # Generate unique filename
            filename = secure_filename(f"{customer_id}_{file.filename}")
            file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)

            # Save file
            file.save(file_path)

            # Update user profile picture
            user.profile_image = filename
            db.session.commit()

            # Invalidate profile cache
            delete_pattern(f"customer:profile:{customer_id}")

            return {"message": "Profile picture updated successfully"}, 200

        return {"message": "Invalid file type"}, 400


@customer_bp.route("/account")
class CustomerAccount(Resource):
    @customer_bp.doc(description="Delete customer account")
    @customer_required()
    def delete(self):
        """Delete customer account."""
        customer_id = get_jwt_identity()
        user = User.query.get_or_404(customer_id)

        # Delete user's profile pictures if any
        if user.profile_image:
            try:
                file_path = os.path.join(
                    current_app.config["UPLOAD_FOLDER"], user.profile_image
                )
                if os.path.exists(file_path):
                    os.remove(file_path)
            except OSError:
                pass  # Ignore errors if file doesn't exist or can't be deleted

        # Delete user
        db.session.delete(user)
        db.session.commit()

        # Invalidate all customer-related caches
        delete_pattern(f"customer:*:{customer_id}")

        return {"message": "Account deleted successfully"}, 200


@customer_bp.route("/dashboard/stats")
class CustomerDashboardStats(Resource):
    @jwt_required()
    @customer_bp.doc(description="Get stats for customer dashboard")
    @customer_required()
    @cache_result("customer:stats:{identity}", expiration=300)
    def get(self):
        """Get statistics for the customer dashboard."""
        customer_id = get_jwt_identity()

        # Get all service requests for the customer
        service_requests = ServiceRequest.query.filter_by(customer_id=customer_id).all()

        total_requests = len(service_requests)
        completed_requests = len(
            [r for r in service_requests if r.service_status.lower() == "completed"]
        )
        pending_requests = len(
            [r for r in service_requests if r.service_status.lower() == "pending"]
        )
        accepted_requests = len(
            [r for r in service_requests if r.service_status.lower() == "accepted"]
        )
        cancelled_requests = len(
            [r for r in service_requests if r.service_status.lower() == "cancelled"]
        )

        # Calculate money spent on completed services
        total_spent = 0
        for request in service_requests:
            if request.service_status.lower() == "completed":
                service = Service.query.get(request.service_id)
                if service:
                    total_spent += service.price

        # Get services by category
        services_data = (
            db.session.query(Service.name, db.func.count(ServiceRequest.id))
            .join(ServiceRequest, ServiceRequest.service_id == Service.id)
            .filter(ServiceRequest.customer_id == customer_id)
            .group_by(Service.name)
            .all()
        )

        services_by_category = [
            {"name": name, "count": count} for name, count in services_data
        ]

        # Return stats
        return {
            "totalRequests": total_requests,
            "completedJobs": completed_requests,
            "pendingJobs": pending_requests,
            "activeJobs": accepted_requests,
            "cancelledJobs": cancelled_requests,
            "totalSpent": float(total_spent),
            "servicesByCategory": services_by_category,
        }


# Helper function to check allowed file extensions
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in {
        "png",
        "jpg",
        "jpeg",
        "gif",
    }
