from flask import Blueprint
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt
from ..models import User, Role, Service, ServiceRequest
from ..database import db
from .auth import admin_required

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
    },
    model_id="admin_service_request_model",
)


@admin_bp.route("/users")
class UserList(Resource):
    @admin_bp.marshal_list_with(user_model)
    @admin_required()
    def get(self):
        """List all users."""
        return User.query.all()


@admin_bp.route("/users/<int:user_id>")
class UserDetail(Resource):
    @admin_bp.marshal_with(user_model)
    @admin_bp.response(404, "User not found")
    @admin_required()
    def get(self, user_id):
        """Get details of a specific user."""
        user = User.query.get_or_404(user_id)
        return user


@admin_bp.route("/roles")
class RoleList(Resource):
    @admin_bp.marshal_list_with(role_model)
    @admin_required()
    def get(self):
        """List all roles."""
        return Role.query.all()


@admin_bp.route("/roles/<int:role_id>")
class RoleDetail(Resource):
    @admin_bp.marshal_with(role_model)
    @admin_bp.response(404, "Role not found")
    @admin_required()
    def get(self, role_id):
        """Get details of a specific role."""
        role = Role.query.get_or_404(role_id)
        return role


@admin_bp.route("/services")
class AdminServiceList(Resource):
    @admin_bp.marshal_list_with(service_model)
    @admin_required()
    def get(self):
        """List all services."""
        return Service.query.all()


@admin_bp.route("/services/<int:service_id>")
class AdminServiceDetail(Resource):
    @admin_bp.marshal_with(service_model)
    @admin_bp.response(404, "Service not found")
    @admin_required()
    def get(self, service_id):
        """Get details of a specific service."""
        service = Service.query.get_or_404(service_id)
        return service


@admin_bp.route("/requests")
class AdminRequestList(Resource):
    @admin_bp.marshal_list_with(service_request_model)
    @admin_required()
    def get(self):
        """List all service requests."""
        return ServiceRequest.query.all()


@admin_bp.route("/requests/<int:request_id>")
class AdminRequestDetail(Resource):
    @admin_bp.marshal_with(service_request_model)
    @admin_bp.response(404, "Request not found")
    @admin_required()
    def get(self, request_id):
        """Get details of a specific service request."""
        request = ServiceRequest.query.get_or_404(request_id)
        return request
