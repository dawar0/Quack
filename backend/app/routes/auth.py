from flask import Blueprint, request, current_app, send_file
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)
from ..models import User, Role, Document
from werkzeug.security import generate_password_hash, check_password_hash
from ..database import db
from werkzeug.utils import secure_filename
from ..tasks.email_tasks import send_welcome_email_task
import os


def admin_required():
    def wrapper(fn):
        @jwt_required()
        def decorator(*args, **kwargs):
            # Skip admin check for OPTIONS requests
            if request.method == "OPTIONS":
                return fn(*args, **kwargs)

            claims = get_jwt()
            if "admin" not in claims.get("roles", []):
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

            # Check if professional is approved
            current_user_id = get_jwt_identity()
            user = User.query.get(int(current_user_id))
            if not user or user.status != "approved":
                return {
                    "message": "Professional must be approved by admin to access this resource"
                }, 403

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
        "email": fields.String(required=True, description="User email"),
        "password": fields.String(required=True, description="User password"),
    },
    model_id="auth_user_credentials",
)

user_registration = auth_bp.model(
    "UserRegistration",
    {
        "username": fields.String(required=True, description="User username"),
        "email": fields.String(required=True, description="User email"),
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


# Public endpoint for serving profile images
@auth_bp.route("/profile-images/<string:filename>")
class PublicProfileImage(Resource):
    @auth_bp.doc(description="Get a user's profile image by filename")
    def get(self, filename):
        """Get a user's profile image by filename."""
        # Secure the filename to prevent directory traversal attacks
        secure_name = secure_filename(filename)

        # Build the path to the profile image
        file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], secure_name)

        # Check if file exists
        if not os.path.exists(file_path):
            # Print debug info to server logs
            print(f"Image not found at path: {file_path}")
            print(f"Upload folder config: {current_app.config['UPLOAD_FOLDER']}")
            print(f"Requested filename: {filename}, Secure name: {secure_name}")
            return {"message": f"Image not found: {secure_name}"}, 404

        # Get file extension and set appropriate MIME type
        file_ext = os.path.splitext(secure_name)[1].lower()
        mime_types = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".gif": "image/gif",
        }
        mimetype = mime_types.get(file_ext, "application/octet-stream")

        # Return the file with cache control headers to avoid browser caching
        response = send_file(file_path, mimetype=mimetype, as_attachment=False)
        response.headers["Cache-Control"] = (
            "no-store, no-cache, must-revalidate, max-age=0"
        )
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response


# Model for login request
login_model = auth_bp.model(
    "Login",
    {
        "username": fields.String(required=True, description="Username"),
        "password": fields.String(required=True, description="Password"),
    },
)


@auth_bp.route("/register")
class Register(Resource):
    @auth_bp.expect(user_registration)
    @auth_bp.response(201, "User created successfully")
    @auth_bp.response(400, "Email already exists")
    def post(self):
        """Register a new user."""
        data = request.form.to_dict()
        files = request.files

        # Check if username already exists
        if User.query.filter_by(username=data.get("username")).first():
            return {"message": "Username already exists"}, 400

        # Check if email already exists
        if User.query.filter_by(email=data.get("email")).first():
            return {"message": "Email already exists"}, 400

        # Create user
        user = User(
            username=data.get("username"),
            password=generate_password_hash(data.get("password")),
            name=data.get("name"),
            email=data.get("email"),
            phone_number=data.get("phone_number"),
            address=data.get("address"),
            service_type=data.get("service_type"),
            experience=data.get("experience"),
            description=data.get("description"),
        )

        # Add role
        role = Role.query.filter_by(name=data.get("role")).first()
        if role:
            user.roles.append(role)

        db.session.add(user)
        db.session.flush()  # Get user ID without committing

        # Handle document uploads
        if files:
            for key, file in files.items():
                if key.startswith("document_"):
                    # Get the index from the key (e.g., 'document_0' -> 0)
                    index = int(key.split("_")[1])
                    document_type = data.get(f"document_type_{index}")

                    if file and allowed_file(file.filename):
                        # Generate unique filename
                        filename = secure_filename(
                            f"{user.id}_{document_type}_{file.filename}"
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
                            user_id=user.id,
                            document_type=document_type,
                            file_name=filename,
                            file_path=file_path,
                        )
                        db.session.add(document)

        db.session.commit()

        # Generate tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        # Send welcome email
        if user.email:
            send_welcome_email_task.delay(user.email, user.name or user.username)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                "id": user.id,
                "username": user.username,
                "name": user.name,
                "email": user.email,
                "roles": [{"id": role.id, "name": role.name} for role in user.roles],
            },
        }


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg", "gif"}
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@auth_bp.route("/login")
class Login(Resource):
    @auth_bp.expect(user_credentials)
    @auth_bp.response(200, "Login successful", tokens)
    @auth_bp.response(401, "Invalid credentials")
    def post(self):
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return {"message": "Email and password are required"}, 401

        user = User.query.filter_by(email=email).first()

        if not user:
            return {"message": "User not found"}, 401

        if not check_password_hash(user.password, password):
            return {"message": "Invalid password"}, 401

        # If we get here, credentials are valid
        roles = [role.name for role in user.roles]
        access_token = create_access_token(
            identity=str(user.id), additional_claims={"roles": roles}
        )
        refresh_token = create_refresh_token(identity=str(user.id))
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "roles": roles,
        }, 200


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
            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "roles": roles,
            }, 200
        return {"message": "Invalid user"}, 401


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
            return {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "name": user.name,
                "roles": [{"id": role.id, "name": role.name} for role in user.roles],
                "phone_number": user.phone_number,
                "address": user.address,
                "service_type": user.service_type,
                "experience": user.experience,
                "description": user.description,
                "profile_docs_verified": user.profile_docs_verified,
                "blocked": user.blocked,
                "status": user.status,
                "rejection_reason": user.rejection_reason,
                "profile_image": user.profile_image,
            }, 200
        return {"message": "User not found"}, 404
