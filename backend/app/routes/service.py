from flask import Blueprint, request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from ..models import Service
from ..database import db
from .auth import admin_required
from ..utils.cache import cache_result, delete_pattern

service_bp = Namespace(
    "service", description="Service management operations (Admin only)"
)

service_model = service_bp.model(
    "Service",
    {
        "id": fields.Integer(readonly=True),
        "name": fields.String(required=True),
        "price": fields.Float(required=True),
        "time_required": fields.String(),
        "description": fields.String(),
    },
    model_id="service_model",
)

service_creation_model = service_bp.model(
    "ServiceCreation",
    {
        "name": fields.String(required=True),
        "price": fields.Float(required=True),
        "time_required": fields.String(),
        "description": fields.String(),
    },
    model_id="service_creation_model",
)

service_update_model = service_bp.model(
    "ServiceUpdate",
    {
        "name": fields.String(),
        "price": fields.Float(),
        "time_required": fields.String(),
        "description": fields.String(),
    },
    model_id="service_update_model",
)


@service_bp.route("/")
class ServiceList(Resource):
    @service_bp.marshal_list_with(service_model)
    @cache_result("service", expiration=600)
    def get(self):
        """List all available services."""
        return Service.query.all()

    @service_bp.expect(service_creation_model, validate=True)
    @service_bp.marshal_with(service_model, code=201)
    @admin_required()
    def post(self):
        """Create a new service (Admin only)."""
        data = request.get_json()
        new_service = Service(
            name=data["name"],
            price=data["price"],
            time_required=data.get("time_required"),
            description=data.get("description"),
        )
        db.session.add(new_service)
        db.session.commit()

        delete_pattern("service:*")

        return new_service, 201


@service_bp.route("/<int:service_id>")
class ServiceDetail(Resource):
    @service_bp.marshal_with(service_model)
    @service_bp.response(404, "Service not found")
    @cache_result("service", expiration=600, args_as_key=True)
    def get(self, service_id):
        """Get details of a specific service."""
        service = Service.query.get_or_404(service_id)
        return service

    @service_bp.expect(service_update_model, validate=True)
    @service_bp.marshal_with(service_model)
    @service_bp.response(404, "Service not found")
    @admin_required()
    def put(self, service_id):
        """Update an existing service (Admin only)."""
        service = Service.query.get_or_404(service_id)
        data = request.get_json()
        if "name" in data:
            service.name = data["name"]
        if "price" in data:
            service.price = data["price"]
        if "time_required" in data:
            service.time_required = data["time_required"]
        if "description" in data:
            service.description = data["description"]
        db.session.commit()

        delete_pattern(f"service:get:{service_id}")
        delete_pattern("service:get")

        return service

    @service_bp.response(204, "Service deleted")
    @service_bp.response(404, "Service not found")
    @service_bp.response(400, "Cannot delete service with existing requests")
    @admin_required()
    def delete(self, service_id):
        """Delete a service (Admin only)."""
        service = Service.query.get_or_404(service_id)

        # Check if there are any service requests for this service
        if service.requests:
            return {"message": "Cannot delete service with existing requests"}, 400

        db.session.delete(service)
        db.session.commit()

        delete_pattern(f"service:get:{service_id}")
        delete_pattern("service:get")

        return "", 204
