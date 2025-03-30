from flask import Blueprint, request, current_app, send_file
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import ServiceRequest, User, Service, Document, Role
from ..database import db
from .auth import professional_required
from datetime import datetime, timedelta
from .customer import service_request_model
from sqlalchemy.orm import joinedload
from werkzeug.utils import secure_filename
import os
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import func, desc
from ..utils.cache import cache_result, delete_pattern
from ..tasks.email_tasks import send_notification_email_task

professional_bp = Namespace(
    "professional", description="Operations for service professionals"
)

user_details_model = professional_bp.model(
    "UserDetails",
    {
        "id": fields.Integer(readonly=True),
        "username": fields.String(required=True),
        "name": fields.String(),
        "email": fields.String(),
        "phone_number": fields.String(),
        "description": fields.String(),
        "experience": fields.String(),
        "service_type": fields.String(),
        "profile_docs_verified": fields.Boolean(),
        "blocked": fields.Boolean(),
        "status": fields.String(),
    },
    model_id="professional_user_details_model",
)

# Register the User model with the namespace
professional_bp.model("User", user_details_model)

service_model = professional_bp.model(
    "Service",
    {
        "id": fields.Integer(readonly=True),
        "name": fields.String(required=True),
        "price": fields.Float(required=True),
        "time_required": fields.String(),
        "description": fields.String(),
    },
    model_id="professional_service_model",
)

service_request_with_details_model = professional_bp.model(
    "ServiceRequestWithDetails",
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
        "customer": fields.Nested(user_details_model),
        "professional": fields.Nested(user_details_model),
        "service": fields.Nested(service_model),
    },
    model_id="professional_service_request_with_details_model",
)

action_on_request_model = professional_bp.model(
    "ActionOnRequest",
    {
        "request_id": fields.Integer(
            required=True, description="ID of the service request"
        ),
        "action": fields.String(
            required=True,
            enum=["accept", "complete"],
            description="Action to take on the request",
        ),
    },
    model_id="professional_action_on_request_model",
)

action_response_model = professional_bp.model(
    "ActionResponse",
    {"message": fields.String(description="Response message")},
    model_id="professional_action_response_model",
)

document_model = professional_bp.model(
    "Document",
    {
        "id": fields.Integer(readonly=True),
        "document_type": fields.String(required=True),
        "file_name": fields.String(readonly=True),
        "upload_date": fields.DateTime(readonly=True),
        "verified": fields.Boolean(readonly=True),
        "rejected": fields.Boolean(readonly=True),
        "rejection_reason": fields.String(readonly=True),
    },
    model_id="professional_document_model",
)

dashboard_stats_model = professional_bp.model(
    "DashboardStats",
    {
        "totalEarnings": fields.Float(description="Total earnings from completed jobs"),
        "completedJobs": fields.Integer(description="Number of completed jobs"),
        "pendingJobs": fields.Integer(description="Number of pending jobs"),
        "acceptedJobs": fields.Integer(description="Number of accepted jobs"),
    },
    model_id="dashboard_stats_model",
)

activity_item_model = professional_bp.model(
    "ActivityItem",
    {
        "id": fields.String(description="Unique identifier for the activity"),
        "type": fields.String(
            description="Type of activity (service_request, payment, etc.)"
        ),
        "action": fields.String(
            description="Action performed (accepted, completed, etc.)"
        ),
        "customer": fields.String(description="Customer name"),
        "customer_id": fields.Integer(description="Customer ID"),
        "customer_profile_image": fields.String(description="Customer profile image"),
        "amount": fields.Float(description="Amount associated with the activity"),
        "timestamp": fields.DateTime(description="When the activity occurred"),
    },
    model_id="activity_item_model",
)


@professional_bp.route("/requests")
class ProfessionalRequests(Resource):
    @professional_bp.marshal_list_with(service_request_with_details_model)
    @professional_bp.doc(description="List all available service requests.")
    @professional_required()
    @cache_result("professional:requests:available", expiration=300)
    def get(self):
        """List all available service requests."""

        requests = (
            ServiceRequest.query.filter_by(professional_id=None)
            .options(
                joinedload(ServiceRequest.customer),
                joinedload(ServiceRequest.service),
            )
            .all()
        )
        return requests


@professional_bp.route("/requests/assigned")
class AssignedProfessionalRequests(Resource):
    @professional_bp.marshal_list_with(service_request_with_details_model)
    @professional_bp.doc(
        description="List all service requests assigned to the logged-in professional."
    )
    @professional_required()
    @cache_result("professional:requests:assigned", expiration=300, args_as_key=True)
    def get(self):
        """List all service requests assigned to the logged-in professional."""
        professional_id = get_jwt_identity()
        return (
            ServiceRequest.query.filter_by(professional_id=professional_id)
            .options(
                joinedload(ServiceRequest.customer),
                joinedload(ServiceRequest.professional),
                joinedload(ServiceRequest.service),
            )
            .all()
        )


@professional_bp.route("/requests/<int:request_id>")
class ProfessionalRequestDetail(Resource):
    @professional_bp.response(404, "Request not found")
    @professional_bp.doc(description="Get details of a specific service request.")
    @professional_bp.marshal_with(service_request_with_details_model)
    @professional_required()
    @cache_result("professional:request", expiration=300, args_as_key=True)
    def get(self, request_id):
        """Get details of a specific service request."""
        professional_id = get_jwt_identity()
        request = ServiceRequest.query.filter_by(
            id=request_id,
        ).first_or_404()
        return request


@professional_bp.route("/requests/take_action")
class TakeActionOnRequest(Resource):
    @professional_bp.expect(action_on_request_model, validate=True)
    @professional_bp.doc(description="Accept or complete a service request.")
    @professional_bp.marshal_with(action_response_model)
    @professional_required()
    def post(self):
        """Accept or complete a service request."""
        data = request.get_json()
        request_id = data.get("request_id")
        action = data.get("action").lower()
        professional_id = get_jwt_identity()

        service_request = ServiceRequest.query.get_or_404(request_id)

        if action == "accept":
            # Only allow accepting if the request has no professional assigned yet
            if service_request.professional_id is not None:
                return (
                    professional_bp.marshal(
                        {
                            "message": "This request has already been assigned to a professional"
                        },
                        action_response_model,
                    ),
                    400,
                )

            service_request.professional_id = professional_id
            service_request.service_status = "Accepted"
            db.session.commit()

            delete_pattern("professional:requests:available")
            delete_pattern(f"professional:requests:assigned:{professional_id}")
            delete_pattern(f"professional:request:{request_id}")
            delete_pattern(f"professional:dashboard:stats:{professional_id}")
            delete_pattern(f"professional:dashboard:activity:{professional_id}")
            delete_pattern(f"customer:requests:{service_request.customer_id}")
            delete_pattern(f"customer:request:{request_id}")
            delete_pattern(f"customer:activity:{service_request.customer_id}")

            # Notify the customer that a professional has accepted their request
            customer = User.query.get(service_request.customer_id)
            if customer and customer.email:
                service_name = (
                    service_request.service.name
                    if service_request.service
                    else "service"
                )
                professional = User.query.get(professional_id)
                professional_name = (
                    professional.name or professional.username
                    if professional
                    else "A professional"
                )

                send_notification_email_task.delay(
                    subject=f"Service Request Accepted - #{request_id}",
                    user_email=customer.email,
                    user_name=customer.name or customer.username,
                    message=f"{professional_name} has accepted your request for {service_name} (Request #{request_id}). "
                    f"They will contact you shortly to arrange the service.",
                )

            return (
                professional_bp.marshal(
                    {"message": f"Request {request_id} has been accepted"},
                    action_response_model,
                ),
                200,
            )

        elif action == "complete":
            # Only allow completion if the request is assigned to this professional
            if service_request.professional_id != professional_id:
                return (
                    professional_bp.marshal(
                        {"message": "This request is not assigned to you"},
                        action_response_model,
                    ),
                    400,
                )

            # Only allow completion if the request is in accepted status
            if service_request.service_status != "Accepted":
                return (
                    professional_bp.marshal(
                        {
                            "message": "This request cannot be completed as it is not in accepted status"
                        },
                        action_response_model,
                    ),
                    400,
                )

            service_request.service_status = "Completed"
            service_request.date_of_completion = datetime.utcnow()
            db.session.commit()

            delete_pattern(f"professional:requests:assigned:{professional_id}")
            delete_pattern(f"professional:request:{request_id}")
            delete_pattern(f"professional:dashboard:stats:{professional_id}")
            delete_pattern(f"professional:dashboard:activity:{professional_id}")
            delete_pattern(f"customer:requests:{service_request.customer_id}")
            delete_pattern(f"customer:request:{request_id}")
            delete_pattern(f"customer:activity:{service_request.customer_id}")

            # Notify the customer that their service request has been completed
            customer = User.query.get(service_request.customer_id)
            if customer and customer.email:
                service_name = (
                    service_request.service.name
                    if service_request.service
                    else "service"
                )
                professional = User.query.get(professional_id)
                professional_name = (
                    professional.name or professional.username
                    if professional
                    else "The professional"
                )

                send_notification_email_task.delay(
                    subject=f"Service Request Completed - #{request_id}",
                    user_email=customer.email,
                    user_name=customer.name or customer.username,
                    message=f"{professional_name} has marked your request for {service_name} (Request #{request_id}) as completed. "
                    f"Thank you for using our services!",
                )

            return (
                professional_bp.marshal(
                    {"message": f"Request {request_id} has been marked as completed"},
                    action_response_model,
                ),
                200,
            )
        else:
            return (
                professional_bp.marshal(
                    {"message": "Invalid action"}, action_response_model
                ),
                400,
            )


@professional_bp.route("/profile")
class ProfessionalProfile(Resource):
    @professional_bp.marshal_with(user_details_model)
    @professional_bp.doc(description="Get professional profile")
    @professional_required()
    @cache_result("professional:profile", expiration=600, args_as_key=True)
    def get(self):
        """Get professional profile"""
        professional_id = get_jwt_identity()
        return User.query.get_or_404(professional_id)

    @professional_bp.expect(user_details_model)
    @professional_bp.marshal_with(user_details_model)
    @professional_required()
    def put(self):
        """Update professional profile."""
        professional_id = get_jwt_identity()
        professional = User.query.get_or_404(professional_id)
        data = request.get_json()

        # Update allowed fields
        allowed_fields = [
            "name",
            "email",
            "phone_number",
            "description",
            "experience",
            "service_type",
        ]
        for field in allowed_fields:
            if field in data:
                setattr(professional, field, data[field])

        db.session.commit()

        delete_pattern(f"professional:profile:{professional_id}")

        return professional


@professional_bp.route("/password")
class ProfessionalPassword(Resource):
    @professional_bp.doc(description="Change professional password")
    @professional_required()
    def put(self):
        """Change professional password."""
        data = request.get_json()
        current_password = data.get("current_password")
        new_password = data.get("new_password")

        if not current_password or not new_password:
            return {"message": "Current password and new password are required"}, 400

        professional_id = get_jwt_identity()
        user = User.query.get_or_404(professional_id)

        if not check_password_hash(user.password, current_password):
            return {"message": "Current password is incorrect"}, 401

        user.password = generate_password_hash(new_password)
        db.session.commit()

        return {"message": "Password updated successfully"}, 200


@professional_bp.route("/profile/picture")
class ProfessionalProfilePicture(Resource):
    @professional_bp.doc(description="Get professional profile picture")
    @professional_required()
    def get(self):
        """Get professional profile picture."""
        professional_id = get_jwt_identity()
        user = User.query.get_or_404(professional_id)

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

    @professional_bp.doc(description="Update professional profile picture")
    @professional_required()
    def put(self):
        """Update professional profile picture."""
        if "profile_picture" not in request.files:
            return {"message": "No profile picture provided"}, 400

        file = request.files["profile_picture"]
        if file.filename == "":
            return {"message": "No selected file"}, 400

        if file and allowed_file(file.filename):
            professional_id = get_jwt_identity()
            user = User.query.get_or_404(professional_id)

            # Generate unique filename
            filename = secure_filename(f"{professional_id}_{file.filename}")
            file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)

            # Save file
            file.save(file_path)

            # Update user profile picture
            user.profile_image = filename
            db.session.commit()

            return {"message": "Profile picture updated successfully"}, 200

        return {"message": "Invalid file type"}, 400


@professional_bp.route("/documents")
class ProfessionalDocuments(Resource):
    @professional_bp.marshal_list_with(document_model)
    @professional_bp.doc(description="Get all documents for the professional")
    @professional_required()
    @cache_result("professional:documents", expiration=600, args_as_key=True)
    def get(self):
        """Get all documents for the professional."""
        professional_id = get_jwt_identity()
        return Document.query.filter_by(user_id=professional_id).all()

    @professional_bp.expect(
        professional_bp.model(
            "DocumentUpload",
            {
                "document_type": fields.String(
                    required=True, enum=["id_proof", "certification", "insurance"]
                ),
            },
            model_id="professional_document_upload_model",
        )
    )
    @professional_bp.marshal_with(document_model)
    @professional_bp.doc(description="Upload a new document")
    @professional_required()
    def post(self):
        """Upload a new document."""
        if "document" not in request.files:
            return {"message": "No document provided"}, 400

        file = request.files["document"]
        document_type = request.form.get("document_type")

        if not document_type or document_type not in [
            "id_proof",
            "certification",
            "insurance",
        ]:
            return {"message": "Invalid document type"}, 400

        if file.filename == "":
            return {"message": "No selected file"}, 400

        if file and allowed_file(file.filename):
            professional_id = get_jwt_identity()

            # Generate unique filename
            filename = secure_filename(
                f"{professional_id}_{document_type}_{file.filename}"
            )
            file_path = os.path.join(
                current_app.config["UPLOAD_FOLDER"], "documents", filename
            )

            # Create documents directory if it doesn't exist
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            # Save file
            file.save(file_path)

            # Create document record
            document = Document(
                user_id=professional_id,
                document_type=document_type,
                file_name=filename,
                file_path=file_path,
            )
            db.session.add(document)
            db.session.commit()

            return document

        return {"message": "Invalid file type"}, 400


@professional_bp.route("/documents/<int:document_id>")
class ProfessionalDocument(Resource):
    @professional_bp.response(404, "Document not found")
    @professional_bp.doc(description="Get a specific document")
    @professional_bp.marshal_with(document_model)
    @professional_required()
    def get(self, document_id):
        """Get a specific document."""
        professional_id = get_jwt_identity()
        document = Document.query.filter_by(
            id=document_id, user_id=professional_id
        ).first_or_404()
        return document

    @professional_bp.response(404, "Document not found")
    @professional_bp.doc(description="Delete a document")
    @professional_required()
    def delete(self, document_id):
        """Delete a document."""
        professional_id = get_jwt_identity()
        document = Document.query.filter_by(
            id=document_id, user_id=professional_id
        ).first_or_404()

        # Delete file from filesystem
        try:
            os.remove(document.file_path)
        except OSError:
            pass  # Ignore if file doesn't exist

        # Delete from database
        db.session.delete(document)
        db.session.commit()

        return {"message": "Document deleted successfully"}, 200


@professional_bp.route("/documents/<int:document_id>/download")
class DownloadProfessionalDocument(Resource):
    @professional_bp.response(404, "Document not found")
    @professional_bp.doc(description="Download a document")
    @professional_required()
    def get(self, document_id):
        """Download a document."""
        professional_id = get_jwt_identity()
        document = Document.query.filter_by(
            id=document_id, user_id=professional_id
        ).first_or_404()

        # Check if file exists
        if not os.path.exists(document.file_path):
            return {"message": "Document file not found on server"}, 404

        # Get file extension
        file_ext = os.path.splitext(document.file_name)[1].lower()

        # Set appropriate MIME type based on file extension
        mime_types = {
            ".pdf": "application/pdf",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".doc": "application/msword",
            ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            ".xls": "application/vnd.ms-excel",
            ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        }

        # Use the appropriate MIME type or default to octet-stream
        mimetype = mime_types.get(file_ext, "application/octet-stream")

        # Return the file
        return send_file(
            document.file_path,
            mimetype=mimetype,
            download_name=document.file_name,
            as_attachment=True,
        )


@professional_bp.route("/dashboard/stats")
class DashboardStats(Resource):
    @professional_bp.marshal_with(dashboard_stats_model)
    @professional_bp.doc(
        description="Get dashboard statistics for the logged-in professional."
    )
    @professional_required()
    @cache_result("professional:dashboard:stats", expiration=300, args_as_key=True)
    def get(self):
        """Get dashboard statistics for the logged-in professional."""
        professional_id = get_jwt_identity()

        # Query for total earnings, completed jobs, and pending jobs
        completed_jobs = ServiceRequest.query.filter_by(
            professional_id=professional_id, service_status="Completed"
        ).all()

        pending_jobs = ServiceRequest.query.filter_by(
            professional_id=professional_id, service_status="Pending"
        ).count()

        accepted_jobs = ServiceRequest.query.filter_by(
            professional_id=professional_id, service_status="Accepted"
        ).count()

        # Calculate total earnings
        total_earnings = 0
        for job in completed_jobs:
            # Get the associated service price
            service = Service.query.get(job.service_id)
            if service:
                total_earnings += service.price

        # Prepare statistics
        stats = {
            "totalEarnings": total_earnings,
            "completedJobs": len(completed_jobs),
            "pendingJobs": pending_jobs,
            "acceptedJobs": accepted_jobs,
        }

        return stats


@professional_bp.route("/dashboard/activity")
class ActivityFeed(Resource):
    @professional_bp.marshal_list_with(activity_item_model)
    @professional_bp.doc(
        description="Get activity feed for the logged-in professional."
    )
    @professional_required()
    @cache_result("professional:dashboard:activity", expiration=300, args_as_key=True)
    def get(self):
        """Get activity feed for the logged-in professional."""
        professional_id = get_jwt_identity()

        # Get the professional's service requests
        requests = (
            ServiceRequest.query.filter_by(professional_id=professional_id)
            .order_by(ServiceRequest.date_of_request.desc())
            .options(
                joinedload(ServiceRequest.customer),
                joinedload(ServiceRequest.service),
            )
            .limit(10)
            .all()
        )

        # Format the activity feed
        activity_feed = []
        for req in requests:
            activity_feed.append(
                {
                    "id": f"sr-{req.id}",
                    "type": "service_request",
                    "action": req.service_status.lower(),
                    "customer": req.customer.name,
                    "customer_id": req.customer_id,
                    "customer_profile_image": req.customer.profile_image,
                    "amount": (
                        float(req.service.price)
                        if req.service_status == "Completed"
                        else 0
                    ),
                    "timestamp": req.date_of_request,
                }
            )

        return activity_feed


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg", "gif"}
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
