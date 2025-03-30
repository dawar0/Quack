from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models.user import User


@auth_bp.route("/logout")
class Logout(Resource):
    @jwt_required()
    @auth_bp.response(200, "Logged out successfully")
    def post(self):
        # For stateless JWT, client-side needs to discard the tokens
        return {"message": "Logged out successfully"}, 200


@auth_bp.route("/me")
class CurrentUser(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        user = User.query.get(int(current_user_id))
        if user:
            return user, 200
        return {"message": "User not found"}, 404
