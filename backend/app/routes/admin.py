from flask import Blueprint, request, Response, send_file
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt
from ..models import (
    User,
    Role,
    Service,
    ServiceRequest,
    Document,
    Admin,
    Customer,
    Professional,
    Notification,
    Review,
    PaymentTransaction,
)
from sqlalchemy.orm import joinedload
from ..database import db
from .auth import admin_required
from datetime import datetime, timedelta
import os
from ..utils.cache_management import (
    get_cache_stats,
    list_cache_keys,
    get_key_info,
    clear_cache,
    get_cache_usage_by_prefix,
)
from ..utils.cache import cache_result, delete_pattern

admin_bp = Namespace("admin", description="Admin operations")

user_model = admin_bp.model(
    "User",
    {
        "id": fields.Integer(readonly=True),
        "username": fields.String(required=True),
        "name": fields.String(),
        "email": fields.String(),
        "phone_number": fields.String(),
        "role_ids": fields.List(fields.Integer),
        "date_created": fields.DateTime(),
        "description": fields.String(),
        "experience": fields.String(),
        "service_type": fields.String(),
        "profile_docs_verified": fields.Boolean(),
        "blocked": fields.Boolean(),
        "status": fields.String(),
        "profile_image": fields.String(),
        "address": fields.String(),
    },
    model_id="admin_user_model",
)

role_model = admin_bp.model(
    "Role",
    {"id": fields.Integer(readonly=True), "name": fields.String(required=True)},
    model_id="admin_role_model",
)

service_model = admin_bp.model(
    "Service",
    {
        "id": fields.Integer(readonly=True),
        "name": fields.String(required=True),
        "price": fields.Float(required=True),
        "time_required": fields.String(),
        "description": fields.String(),
    },
    model_id="admin_service_model",
)

user_details_model = admin_bp.model(
    "UserDetails",
    {
        "id": fields.Integer(readonly=True),
        "username": fields.String(required=True),
        "name": fields.String(),
        "email": fields.String(),
        "phone_number": fields.String(),
        "role_ids": fields.List(fields.Integer),
        "date_created": fields.DateTime(),
        "description": fields.String(),
        "experience": fields.String(),
        "service_type": fields.String(),
        "profile_docs_verified": fields.Boolean(),
        "blocked": fields.Boolean(),
        "status": fields.String(),
    },
    model_id="admin_user_details_model",
)

service_request_model = admin_bp.model(
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
        "customer": fields.Nested(user_details_model),
        "professional": fields.Nested(user_details_model),
        "service": fields.Nested(service_model),
    },
    model_id="admin_service_request_model",
)

document_model = admin_bp.model(
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
    model_id="admin_document_model",
)

# Add a cache management namespace within the admin namespace
cache_ns = admin_bp.namespace("cache", description="Cache management operations")


@cache_ns.route("/stats")
class CacheStats(Resource):
    @admin_required()
    def get(self):
        """Get cache statistics (Admin only)"""
        return get_cache_stats()


@cache_ns.route("/keys")
class CacheKeys(Resource):
    @admin_required()
    @cache_ns.param("pattern", 'Key pattern to filter (e.g. "service:*")', default="*")
    def get(self):
        """List cache keys with optional pattern filter (Admin only)"""
        pattern = request.args.get("pattern", "*")
        return {"keys": list_cache_keys(pattern)}


@cache_ns.route("/key/<string:key>")
class CacheKeyInfo(Resource):
    @admin_required()
    def get(self, key):
        """Get information about a specific cache key (Admin only)"""
        return get_key_info(key)

    @admin_required()
    def delete(self, key):
        """Delete a specific cache key (Admin only)"""
        from ..utils.cache import delete_cache

        success = delete_cache(key)
        return {"success": success}


@cache_ns.route("/clear")
class CacheClear(Resource):
    @admin_required()
    @cache_ns.param("pattern", 'Key pattern to clear (e.g. "service:*")', default="*")
    def delete(self):
        """Clear cache entries matching pattern (Admin only)"""
        pattern = request.args.get("pattern", "*")
        deleted_count = clear_cache(pattern)
        return {"deleted_count": deleted_count}


@cache_ns.route("/usage")
class CacheUsage(Resource):
    @admin_required()
    def get(self):
        """Get cache usage statistics grouped by prefix (Admin only)"""
        return {"usage_by_prefix": get_cache_usage_by_prefix()}


@admin_bp.route("/users")
class UserList(Resource):
    @admin_bp.marshal_list_with(user_model)
    @admin_required()
    @cache_result("admin:users", expiration=300)
    def get(self):
        """List all users."""
        return User.query.all()


@admin_bp.route("/users/<int:user_id>")
class UserDetail(Resource):
    @admin_bp.marshal_with(user_model)
    @admin_bp.response(404, "User not found")
    @admin_required()
    @cache_result("admin:user", expiration=300, args_as_key=True)
    def get(self, user_id):
        """Get details of a specific user."""
        user = User.query.get_or_404(user_id)
        return user


@admin_bp.route("/roles")
class RoleList(Resource):
    @admin_bp.marshal_list_with(role_model)
    @admin_required()
    @cache_result("admin:roles", expiration=3600)
    def get(self):
        """List all roles."""
        return Role.query.all()


@admin_bp.route("/roles/<int:role_id>")
class RoleDetail(Resource):
    @admin_bp.marshal_with(role_model)
    @admin_bp.response(404, "Role not found")
    @admin_required()
    @cache_result("admin:role", expiration=3600, args_as_key=True)
    def get(self, role_id):
        """Get details of a specific role."""
        role = Role.query.get_or_404(role_id)
        return role


@admin_bp.route("/services")
class AdminServiceList(Resource):
    @admin_bp.marshal_list_with(service_model)
    @admin_required()
    @cache_result("admin:services", expiration=600)
    def get(self):
        """List all services."""
        return Service.query.all()


@admin_bp.route("/services/<int:service_id>")
class AdminServiceDetail(Resource):
    @admin_bp.marshal_with(service_model)
    @admin_bp.response(404, "Service not found")
    @admin_required()
    @cache_result("admin:service", expiration=600, args_as_key=True)
    def get(self, service_id):
        """Get details of a specific service."""
        service = Service.query.get_or_404(service_id)
        return service


@admin_bp.route("/requests")
class AdminRequestList(Resource):
    @admin_bp.marshal_list_with(service_request_model)
    @admin_required()
    @cache_result("admin:requests", expiration=300)
    def get(self):
        """List all service requests."""
        return ServiceRequest.query.options(
            joinedload(ServiceRequest.customer),
            joinedload(ServiceRequest.professional),
            joinedload(ServiceRequest.service),
        ).all()


@admin_bp.route("/requests/<int:request_id>")
class AdminRequestDetail(Resource):
    @admin_bp.marshal_with(service_request_model)
    @admin_bp.response(404, "Request not found")
    @admin_required()
    @cache_result("admin:request", expiration=300, args_as_key=True)
    def get(self, request_id):
        """Get details of a specific service request."""
        request = ServiceRequest.query.get_or_404(request_id)
        return request


@admin_bp.route("/requests/<int:request_id>/status")
class RequestStatusUpdate(Resource):
    @admin_bp.expect(
        admin_bp.model(
            "RequestStatus",
            {
                "status": fields.String(
                    required=True,
                    enum=["Pending", "Accepted", "Completed", "Cancelled"],
                )
            },
        )
    )
    @admin_bp.marshal_with(service_request_model)
    @admin_bp.response(404, "Request not found")
    @admin_required()
    def patch(self, request_id):
        """Update service request status."""
        request = ServiceRequest.query.get_or_404(request_id)
        data = request.get_json()
        request.service_status = data.get("status", request.service_status)
        db.session.commit()

        delete_pattern(f"admin:request:{request_id}")
        delete_pattern("admin:requests")
        delete_pattern("admin:dashboard:stats")

        if request.customer_id:
            delete_pattern(f"customer:requests:{request.customer_id}")
            delete_pattern(f"customer:request:{request_id}")
            delete_pattern(f"customer:activity:{request.customer_id}")

        if request.professional_id:
            delete_pattern(f"professional:requests:assigned:{request.professional_id}")
            delete_pattern(f"professional:request:{request_id}")
            delete_pattern(f"professional:dashboard:stats:{request.professional_id}")
            delete_pattern(f"professional:dashboard:activity:{request.professional_id}")

        return request


@admin_bp.route("/dashboard/stats")
class DashboardStats(Resource):
    @admin_required()
    @cache_result("admin:dashboard:stats", expiration=300)
    def get(self):
        """Get dashboard statistics."""
        stats = {
            "total_customers": User.query.filter(
                User.roles.any(Role.name == "customer")
            ).count(),
            "total_professionals": User.query.filter(
                User.roles.any(Role.name == "professional")
            ).count(),
            "active_services": Service.query.count(),
            "pending_requests": ServiceRequest.query.filter_by(
                service_status="Pending"
            ).count(),
            "accepted_requests": ServiceRequest.query.filter_by(
                service_status="Accepted"
            ).count(),
            "completed_services": ServiceRequest.query.filter_by(
                service_status="Completed"
            ).count(),
            "recent_activity": [
                {
                    "id": req.id,
                    "type": "service_request",
                    "title": f"Service Request #{req.id}",
                    "description": f"New service request for {req.service.name} from {req.customer.name}",
                    "timestamp": req.date_of_request.isoformat(),
                    "status": req.service_status,
                    "amount": req.service.price if req.service else 0,
                    "customer_id": req.customer.id,
                    "customer_name": req.customer.name,
                    "customer_profile_image": req.customer.profile_image,
                }
                for req in ServiceRequest.query.order_by(
                    ServiceRequest.date_of_request.desc()
                )
                .limit(5)
                .all()
            ]
            + [
                {
                    "id": user.id,
                    "type": "user_registration",
                    "title": f"New {role.name.title()} Registration",
                    "description": f"{user.name} registered as a {role.name}",
                    "timestamp": user.date_created.isoformat(),
                    "status": "active",
                    "user_id": user.id,
                    "user_name": user.name,
                    "user_profile_image": user.profile_image,
                }
                for user, role in db.session.query(User, Role)
                .join(User.roles)
                .filter(User.date_created >= datetime.utcnow() - timedelta(days=7))
                .order_by(User.date_created.desc())
                .limit(5)
                .all()
            ],
        }
        return stats


@admin_bp.route("/users/<int:user_id>/status")
class UserStatusUpdate(Resource):
    @admin_bp.expect(
        admin_bp.model(
            "UserStatus",
            {
                "status": fields.String(enum=["pending", "approved", "disapproved"]),
                "blocked": fields.Boolean(),
                "rejection_reason": fields.String(required=False),
            },
        )
    )
    @admin_bp.marshal_with(user_model)
    @admin_bp.response(404, "User not found")
    @admin_required()
    def patch(self, user_id):
        """Update user status (approval/disapproval) and blocked state."""
        try:
            user = User.query.get_or_404(user_id)
            data = request.get_json()

            if data is None:
                return {"message": "Invalid JSON data"}, 400

            # Validate data structure
            if not isinstance(data, dict):
                return {"message": "Data must be a JSON object"}, 400

            # Validate and update status if provided
            if "status" in data:
                status = data["status"]
                if not isinstance(status, str):
                    return {"message": "Status must be a string"}, 400
                if status not in ["pending", "approved", "disapproved"]:
                    return {"message": "Invalid status value"}, 400
                user.status = status

                # Add rejection reason if status is disapproved
                if status == "disapproved" and "rejection_reason" in data:
                    user.rejection_reason = data["rejection_reason"]

            # Validate and update blocked state if provided
            if "blocked" in data:
                blocked = data["blocked"]
                if not isinstance(blocked, bool):
                    return {"message": "Blocked must be a boolean value"}, 400
                user.blocked = blocked

            db.session.commit()

            # Invalidate caches
            delete_pattern(f"admin:user:{user_id}")
            delete_pattern("admin:users")

            # Invalidate user-specific caches based on role
            professional = Professional.query.filter_by(user_id=user_id).first()
            customer = Customer.query.filter_by(user_id=user_id).first()

            if professional:
                delete_pattern(f"professional:profile:{user_id}")
            if customer:
                delete_pattern(f"customer:profile:{user_id}")

            return user
        except Exception as e:
            db.session.rollback()
            return {"message": f"Error updating user status: {str(e)}"}, 500


@admin_bp.route("/reports")
class Reports(Resource):
    @admin_required()
    def get(
        self,
    ):
        """Get reports data based on type and date range."""
        report_type = request.args.get("type", "service")
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")

        if not start_date or not end_date:
            return {"message": "Start date and end date are required"}, 400

        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            return {"message": "Invalid date format. Use YYYY-MM-DD"}, 400

        if report_type == "service":
            # Get service requests data
            requests = (
                ServiceRequest.query.filter(
                    ServiceRequest.date_of_request.between(start_date, end_date)
                )
                .options(
                    joinedload(ServiceRequest.customer),
                    joinedload(ServiceRequest.service),
                    joinedload(ServiceRequest.professional),
                )
                .all()
            )

            # Group by month
            service_requests = {}
            for service_request in requests:
                month = service_request.date_of_request.strftime("%Y-%m")
                if month not in service_requests:
                    service_requests[month] = {
                        "month": month,
                        "requested": 0,
                        "completed": 0,
                        "cancelled": 0,
                    }
                service_requests[month]["requested"] += 1
                if service_request.service_status == "Completed":
                    service_requests[month]["completed"] += 1
                elif service_request.service_status == "Cancelled":
                    service_requests[month]["cancelled"] += 1

            # Get service type distribution
            service_types = {}
            for service_request in requests:
                service_name = service_request.service.name
                if service_name not in service_types:
                    service_types[service_name] = 0
                service_types[service_name] += 1

            return {
                "service_requests": list(service_requests.values()),
                "service_types": [
                    {"service": name, "count": count}
                    for name, count in service_types.items()
                ],
            }

        elif report_type == "professional":
            # Get professional statistics
            professionals = User.query.filter(
                User.roles.any(Role.name == "professional")
            ).all()

            total_professionals = len(professionals)
            pending_approvals = len([p for p in professionals if p.status == "pending"])
            active_professionals = len(
                [p for p in professionals if p.status == "approved" and not p.blocked]
            )
            blocked_professionals = len([p for p in professionals if p.blocked])

            # Get service statistics
            total_services = ServiceRequest.query.filter(
                ServiceRequest.professional_id.in_([p.id for p in professionals])
            ).count()

            completed_services = ServiceRequest.query.filter(
                ServiceRequest.professional_id.in_([p.id for p in professionals]),
                ServiceRequest.status == "Completed",
            ).count()

            active_services = ServiceRequest.query.filter(
                ServiceRequest.professional_id.in_([p.id for p in professionals]),
                ServiceRequest.status.in_(["Pending", "Approved"]),
            ).count()

            return {
                "professional_stats": {
                    "total_professionals": total_professionals,
                    "pending_approvals": pending_approvals,
                    "active_professionals": active_professionals,
                    "blocked_professionals": blocked_professionals,
                    "total_services": total_services,
                    "completed_services": completed_services,
                    "active_services": active_services,
                }
            }

        elif report_type == "customer":
            # Get customer activity data
            customers = User.query.filter(User.roles.any(Role.name == "customer")).all()

            customer_activity = []
            for customer in customers:
                requests = (
                    ServiceRequest.query.filter_by(customer_id=customer.id)
                    .filter(
                        ServiceRequest.date_of_request.between(start_date, end_date)
                    )
                    .all()
                )

                total_requests = len(requests)
                completed = sum(1 for r in requests if r.service_status == "Completed")
                cancelled = sum(1 for r in requests if r.service_status == "Cancelled")
                total_spent = sum(
                    r.service.price for r in requests if r.service_status == "Completed"
                )
                last_request = max((r.date_of_request for r in requests), default=None)

                customer_activity.append(
                    {
                        "customer": customer.name,
                        "profile_image": customer.profile_image,
                        "total_requests": total_requests,
                        "completed": completed,
                        "cancelled": cancelled,
                        "total_spent": total_spent,
                        "last_request": (
                            last_request.strftime("%Y-%m-%d") if last_request else None
                        ),
                    }
                )

            return {
                "customer_activity": sorted(
                    customer_activity, key=lambda x: x["total_requests"], reverse=True
                )[:10]
            }

        return {"message": "Invalid report type"}, 400


@admin_bp.route("/reports/export")
class ExportReport(Resource):
    @admin_required()
    def get(self):
        """Export report data as CSV."""
        report_type = request.args.get("type", "service")
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")

        if not start_date or not end_date:
            return {"message": "Start date and end date are required"}, 400

        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            return {"message": "Invalid date format. Use YYYY-MM-DD"}, 400

        # Get the report data
        report_data = self.get_report_data(report_type, start_date, end_date)
        if isinstance(report_data, tuple):  # Error response
            return report_data

        # Convert to CSV
        import csv
        import io

        output = io.StringIO()
        writer = csv.writer(output)

        if report_type == "service":
            # Write service requests data
            writer.writerow(["Month", "Requested", "Completed", "Cancelled"])
            for row in report_data["service_requests"]:
                writer.writerow(
                    [row["month"], row["requested"], row["completed"], row["cancelled"]]
                )

            writer.writerow([])  # Empty row for separation

            # Write service types data
            writer.writerow(["Service Type", "Count"])
            for row in report_data["service_types"]:
                writer.writerow([row["service"], row["count"]])

        elif report_type == "professional":
            writer.writerow(["Rating", "Count"])
            for row in report_data["professional_ratings"]:
                writer.writerow([row["rating"], row["count"]])

        elif report_type == "customer":
            writer.writerow(
                [
                    "Customer",
                    "Profile Image",
                    "Total Requests",
                    "Completed",
                    "Cancelled",
                    "Total Spent",
                    "Last Request",
                ]
            )
            for row in report_data["customer_activity"]:
                writer.writerow(
                    [
                        row["customer"],
                        row["profile_image"] or "N/A",
                        row["total_requests"],
                        row["completed"],
                        row["cancelled"],
                        row["total_spent"],
                        row["last_request"],
                    ]
                )

        output.seek(0)
        return Response(
            output.getvalue(),
            mimetype="text/csv",
            headers={
                "Content-Disposition": f'attachment; filename=report_{report_type}_{start_date.strftime("%Y%m%d")}_{end_date.strftime("%Y%m%d")}.csv'
            },
        )

    def get_report_data(self, report_type, start_date, end_date):
        """Helper method to get report data."""
        if report_type == "service":
            requests = ServiceRequest.query.filter(
                ServiceRequest.date_of_request.between(start_date, end_date)
            ).all()

            service_requests = {}
            for service_request in requests:
                month = service_request.date_of_request.strftime("%Y-%m")
                if month not in service_requests:
                    service_requests[month] = {
                        "month": month,
                        "requested": 0,
                        "completed": 0,
                        "cancelled": 0,
                    }
                service_requests[month]["requested"] += 1
                if service_request.service_status == "Completed":
                    service_requests[month]["completed"] += 1
                elif service_request.service_status == "Cancelled":
                    service_requests[month]["cancelled"] += 1

            service_types = {}
            for service_request in requests:
                service_name = service_request.service.name
                if service_name not in service_types:
                    service_types[service_name] = 0
                service_types[service_name] += 1

            return {
                "service_requests": list(service_requests.values()),
                "service_types": [
                    {"service": name, "count": count}
                    for name, count in service_types.items()
                ],
            }

        elif report_type == "professional":
            professionals = User.query.filter(
                User.roles.any(Role.name == "professional")
            ).all()

            ratings = {}
            for prof in professionals:
                rating = round(prof.rating or 0)
                if rating not in ratings:
                    ratings[rating] = 0
                ratings[rating] += 1

            return {
                "professional_ratings": [
                    {"rating": rating, "count": count}
                    for rating, count in sorted(ratings.items())
                ]
            }

        elif report_type == "customer":
            customers = User.query.filter(User.roles.any(Role.name == "customer")).all()

            customer_activity = []
            for customer in customers:
                requests = (
                    ServiceRequest.query.filter_by(customer_id=customer.id)
                    .filter(
                        ServiceRequest.date_of_request.between(start_date, end_date)
                    )
                    .all()
                )

                total_requests = len(requests)
                completed = sum(1 for r in requests if r.service_status == "Completed")
                cancelled = sum(1 for r in requests if r.service_status == "Cancelled")
                total_spent = sum(
                    r.service.price for r in requests if r.service_status == "Completed"
                )
                last_request = max((r.date_of_request for r in requests), default=None)

                customer_activity.append(
                    {
                        "customer": customer.name,
                        "profile_image": customer.profile_image,
                        "total_requests": total_requests,
                        "completed": completed,
                        "cancelled": cancelled,
                        "total_spent": total_spent,
                        "last_request": (
                            last_request.strftime("%Y-%m-%d") if last_request else None
                        ),
                    }
                )

            return {
                "customer_activity": sorted(
                    customer_activity, key=lambda x: x["total_requests"], reverse=True
                )[
                    :10
                ]  # Top 10 customers
            }

        return {"message": "Invalid report type"}, 400


@admin_bp.route("/users/<int:user_id>/documents")
class UserDocuments(Resource):
    @admin_bp.marshal_list_with(document_model)
    @admin_bp.doc(description="Get all documents for a user")
    @admin_required()
    @cache_result("admin:user:documents", expiration=600, args_as_key=True)
    def get(self, user_id):
        """Get all documents for a user."""
        user = User.query.get_or_404(user_id)
        return Document.query.filter_by(user_id=user_id).all()


@admin_bp.route("/documents/<int:document_id>/verify")
class VerifyDocument(Resource):
    @admin_bp.marshal_with(document_model)
    @admin_bp.doc(description="Verify a document")
    @admin_required()
    def patch(self, document_id):
        """Verify a document."""
        document = Document.query.get_or_404(document_id)
        document.verified = True
        document.rejected = False
        document.rejection_reason = None

        # If this is the first verified document for the user,
        # set profile_docs_verified to True
        user = User.query.get(document.user_id)
        if user and not user.profile_docs_verified:
            user.profile_docs_verified = True

        db.session.commit()

        delete_pattern(f"admin:user:{document.user_id}")
        delete_pattern("admin:users")
        delete_pattern(f"admin:user:documents:{document.user_id}")

        professional = Professional.query.filter_by(user_id=document.user_id).first()
        if professional:
            delete_pattern(f"professional:profile:{document.user_id}")
            delete_pattern(f"professional:documents:{document.user_id}")

        return document


@admin_bp.route("/documents/<int:document_id>/reject")
class RejectDocument(Resource):
    @admin_bp.expect(
        admin_bp.model(
            "RejectionReason",
            {
                "reason": fields.String(
                    required=False, description="Reason for rejection"
                ),
            },
        )
    )
    @admin_bp.marshal_with(document_model)
    @admin_bp.doc(description="Reject a document")
    @admin_required()
    def patch(self, document_id):
        """Reject a document."""
        document = Document.query.get_or_404(document_id)
        data = request.get_json() or {}

        document.verified = False
        document.rejected = True
        document.rejection_reason = data.get("reason")

        db.session.commit()

        delete_pattern(f"admin:user:{document.user_id}")
        delete_pattern("admin:users")
        delete_pattern(f"admin:user:documents:{document.user_id}")

        professional = Professional.query.filter_by(user_id=document.user_id).first()
        if professional:
            delete_pattern(f"professional:profile:{document.user_id}")
            delete_pattern(f"professional:documents:{document.user_id}")

        return document


@admin_bp.route("/documents/<int:document_id>/download")
class DownloadDocument(Resource):
    @admin_bp.response(404, "Document not found")
    @admin_bp.doc(description="Download a document")
    @admin_required()
    def get(self, document_id):
        """Download a document."""
        document = Document.query.get_or_404(document_id)

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
