from flask import Blueprint, request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import Service, ServiceRequest
from ..database import db
from .auth import customer_required

customer_bp = Namespace("customer", description="Customer operations")

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
    },
    model_id="customer_service_request_model",
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
        return new_request, 201

    @jwt_required()
    @customer_bp.marshal_list_with(service_request_model)
    def get(self):
        """List all service requests for the logged-in customer."""
        customer_id = get_jwt_identity()
        return ServiceRequest.query.filter_by(customer_id=customer_id).all()


@customer_bp.route("/requests/<int:request_id>")
class CustomerRequestDetail(Resource):
    @jwt_required()
    @customer_bp.marshal_with(service_request_model)
    @customer_bp.response(404, "Request not found")
    def get(self, request_id):
        """Get details of a specific service request for the logged-in customer."""
        customer_id = get_jwt_identity()
        request = ServiceRequest.query.filter_by(
            id=request_id, customer_id=customer_id
        ).first_or_404()
        return request
