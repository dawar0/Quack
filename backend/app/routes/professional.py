from flask import Blueprint, request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import ServiceRequest
from ..database import db
from .auth import professional_required
from datetime import datetime
from .customer import service_request_model

professional_bp = Namespace(
    "professional", description="Operations for service professionals"
)


action_on_request_model = professional_bp.model(
    "ActionOnRequest",
    {
        "request_id": fields.Integer(
            required=True, description="ID of the service request"
        ),
        "action": fields.String(
            required=True,
            enum=["accept", "reject", "complete"],
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


@professional_bp.route("/requests")
class ProfessionalRequests(Resource):
    @professional_bp.marshal_list_with(service_request_model)
    @professional_bp.doc(description="List all available service requests.")
    @professional_required()
    def get(self):
        """List all available service requests."""
        # You might want to filter requests based on the professional's service type or location
        return ServiceRequest.query.filter_by(professional_id=None).all()


@professional_bp.route("/requests/assigned")
class AssignedProfessionalRequests(Resource):
    @professional_bp.marshal_list_with(service_request_model)
    @professional_bp.doc(
        description="List all service requests assigned to the logged-in professional."
    )
    @professional_required()
    def get(self):
        """List all service requests assigned to the logged-in professional."""
        professional_id = get_jwt_identity()
        return ServiceRequest.query.filter_by(professional_id=professional_id).all()


@professional_bp.route("/requests/<int:request_id>")
class ProfessionalRequestDetail(Resource):
    @professional_bp.response(404, "Request not found")
    @professional_bp.doc(description="Get details of a specific service request.")
    @professional_bp.marshal_with(service_request_model)
    @professional_required()
    def get(self, request_id):
        """Get details of a specific service request."""
        professional_id = get_jwt_identity()
        request = ServiceRequest.query.filter_by(
            id=request_id, professional_id=professional_id
        ).first_or_404()
        return request


@professional_bp.route("/requests/take_action")
class TakeActionOnRequest(Resource):
    @professional_bp.expect(action_on_request_model, validate=True)
    @professional_bp.doc(description="Accept, reject, or complete a service request.")
    @professional_bp.marshal_with(action_response_model)
    @professional_required()
    def post(self):
        """Accept, reject, or complete a service request."""
        data = request.get_json()
        request_id = data.get("request_id")
        action = data.get("action")
        professional_id = get_jwt_identity()
        service_request = ServiceRequest.query.get_or_404(request_id)

        if (
            service_request.professional_id is not None
            and service_request.professional_id != professional_id
        ):
            return (
                professional_bp.marshal(
                    {"message": "Request is already assigned to another professional"},
                    action_response_model,
                ),
                403,
            )

        if action == "accept":
            service_request.professional_id = professional_id
            service_request.service_status = "accepted"
        elif action == "reject":
            service_request.professional_id = None
            service_request.service_status = "rejected"
        elif action == "complete":
            service_request.service_status = "completed"
            service_request.date_of_completion = datetime.utcnow()
        else:
            return (
                professional_bp.marshal(
                    {"message": "Invalid action"}, action_response_model
                ),
                400,
            )

        db.session.commit()
        return (
            professional_bp.marshal(
                {"message": f"Request {request_id} updated to {action}"},
                action_response_model,
            ),
            200,
        )
