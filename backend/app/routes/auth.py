from flask import Blueprint, request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)
from ..models import User, Role
from werkzeug.security import generate_password_hash, check_password_hash
from ..database import db


def admin_required():
    def wrapper(fn):
        @jwt_required()
        def decorator(*args, **kwargs):
            claims = get_jwt()
            if "admin" not in claims.get(
                "roles",
            ):
                return {"message": "Admin role required"}, 403
            return fn(*args, **kwargs)

        return decorator

    return wrapper


def professional_required():
    def wrapper(fn):
        @jwt_required()
        def decorator(*args, **kwargs):
            claims = get_jwt()
            if "professional" not in claims.get(
                "roles",
            ):
                return {"message": "Professional role required"}, 403
            return fn(*args, **kwargs)

        return decorator

    return wrapper


def customer_required():
    def wrapper(fn):
        @jwt_required()
        def decorator(*args, **kwargs):
            claims = get_jwt()
            if "customer" not in claims.get(
                "roles",
            ):
                return {"message": "Customer role required"}, 403
            return fn(*args, **kwargs)

        return decorator

    return wrapper


auth_bp = Namespace("auth", description="Authentication operations")

# Models for request and response
user_credentials = auth_bp.model(
    "UserCredentials",
    {
        "username": fields.String(required=True, description="User username"),
        "password": fields.String(required=True, description="User password"),
    },
    model_id="auth_user_credentials",
)

user_registration = auth_bp.model(
    "UserRegistration",
    {
        "username": fields.String(required=True, description="User username"),
        "password": fields.String(required=True, description="User password"),
        "role": fields.String(
            required=True, description="User role (professional/customer)"
        ),
        # Add other registration fields as needed (name, email, etc.)
    },
    model_id="auth_user_registration",
)

tokens = auth_bp.model(
    "Tokens",
    {
        "access_token": fields.String(description="Access token"),
        "refresh_token": fields.String(description="Refresh token"),
    },
    model_id="auth_tokens",
)


@auth_bp.route("/register")
class Register(Resource):
    @auth_bp.expect(user_registration)
    @auth_bp.response(201, "User created successfully")
    @auth_bp.response(400, "Username already exists")
    def post(self):
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        role_name = data.get("role")

        if User.query.filter_by(username=username).first():
            return {"message": "Username already exists"}, 400

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)

        # Assign the role
        role = Role.query.filter_by(name=role_name).first()
        if role:
            new_user.roles.append(role)

        db.session.add(new_user)
        db.session.commit()
        return {"message": "User created successfully"}, 201


@auth_bp.route("/login")
class Login(Resource):
    @auth_bp.expect(user_credentials)
    @auth_bp.marshal_with(tokens)
    @auth_bp.response(401, "Invalid credentials")
    def post(self):
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            roles = [role.name for role in user.roles]
            access_token = create_access_token(
                identity=str(user.id), additional_claims={"roles": roles}
            )
            refresh_token = create_refresh_token(identity=str(user.id))
            response = {"access_token": access_token, "refresh_token": refresh_token}
            return response, 200
        else:
            return {"message": "Invalid credentials"}, 401


@auth_bp.route("/admin/login")
class AdminLogin(Resource):
    @auth_bp.expect(user_credentials)
    @auth_bp.marshal_with(tokens)
    @auth_bp.response(401, "Invalid credentials")
    def post(self):
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        admin = User.query.filter_by(username=username).first()

        if (
            admin
            and check_password_hash(admin.password, password)
            and "admin" in [role.name for role in admin.roles]
        ):
            roles = [role.name for role in admin.roles]
            access_token = create_access_token(
                identity=str(admin.id), additional_claims={"roles": roles}
            )
            refresh_token = create_refresh_token(identity=str(admin.id))
            return {"access_token": access_token, "refresh_token": refresh_token}, 200
        else:
            return {"message": "Invalid credentials or not an admin"}, 401


@auth_bp.route("/refresh")
class Refresh(Resource):
    @jwt_required(refresh=True)
    @auth_bp.marshal_with(tokens)
    def post(self):
        current_user_id = get_jwt_identity()
        user = User.query.get(int(current_user_id))
        if user:
            roles = [role.name for role in user.roles]
            access_token = create_access_token(
                identity=str(current_user_id), additional_claims={"roles": roles}
            )
            refresh_token = create_refresh_token(identity=str(current_user_id))
            return {"access_token": access_token, "refresh_token": refresh_token}, 200
        return {"message": "Invalid user"}, 401


@auth_bp.route("/logout")
class Logout(Resource):
    @jwt_required()
    @auth_bp.response(200, "Logged out successfully")
    def post(self):
        # For stateless JWT, client-side needs to discard the tokens
        return {"message": "Logged out successfully"}, 200
