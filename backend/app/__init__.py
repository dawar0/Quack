from flask import Flask
from .config import Config
from .database import db, init_app
from flask_migrate import Migrate
from .celery_utils import celery_app, init_celery
from flask_restx import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_jwt_extended.exceptions import NoAuthorizationError, InvalidHeaderError
from .utils.email import init_mail
import os

from .routes.admin import admin_bp, cache_ns
from .routes.customer import customer_bp
from .routes.professional import professional_bp
from .routes.service import service_bp
from .routes.auth import auth_bp

from .cli import register_cli_commands


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    upload_folder = os.path.join(app.root_path, "static", "uploads", "profiles")
    os.makedirs(upload_folder, exist_ok=True)
    app.config["UPLOAD_FOLDER"] = upload_folder

    documents_folder = os.path.join(app.root_path, "static", "uploads", "documents")
    os.makedirs(documents_folder, exist_ok=True)

    CORS(
        app,
        resources={
            r"/*": {
                "origins": ["http://localhost:5173"],
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
                "allow_headers": ["Content-Type", "Authorization", "Accept"],
                "expose_headers": ["Content-Type", "Authorization"],
                "supports_credentials": True,
                "max_age": 3600,
            }
        },
    )

    init_app(app)
    migrate = Migrate(app, db)
    init_celery(app)
    init_mail(app)

    api = Api(
        app,
        version="1.0",
        title="Household Services API",
        description="A comprehensive platform for home servicing and solutions.",
        doc="/swagger",
        authorizations={
            "apikey": {
                "type": "apiKey",
                "in": "header",
                "name": "Authorization",
                "description": "Type in the *'Value'* input box below: **'Bearer &lt;JWT&gt;'**, where JWT is the token",
            }
        },
        security="apikey",
    )

    jwt = JWTManager(app)

    @jwt.unauthorized_loader
    def unauthorized_callback(error):
        return {"message": "Missing Authorization Header"}, 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return {"message": "Invalid token"}, 401

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return {"message": "Token has expired"}, 401

    app.config["JWT_TOKEN_LOCATION"] = ["headers"]
    app.config["JWT_HEADER_NAME"] = "Authorization"
    app.config["JWT_HEADER_TYPE"] = "Bearer"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 3600
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = 604800
    app.config["JWT_COOKIE_SECURE"] = False
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False
    app.config["JWT_COOKIE_SAMESITE"] = "Lax"

    api.add_namespace(admin_bp, path="/admin")
    api.add_namespace(cache_ns)
    api.add_namespace(customer_bp, path="/customer")
    api.add_namespace(professional_bp, path="/professional")
    api.add_namespace(service_bp, path="/service")
    api.add_namespace(auth_bp, path="/auth")

    register_cli_commands(app)

    return app


from . import models
