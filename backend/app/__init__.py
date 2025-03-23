from flask import Flask
from .config import Config
from .database import db, init_app
from flask_migrate import Migrate
from .celery_utils import celery_app, init_celery
from flask_restx import Api
from flask_jwt_extended import JWTManager

# Import blueprints
from .routes.admin import admin_bp
from .routes.customer import customer_bp
from .routes.professional import professional_bp
from .routes.service import service_bp
from .routes.auth import auth_bp


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    init_app(app)
    migrate = Migrate(app, db)
    init_celery(app)

    # Initialize Flask-RESTx API
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

    # Initialize Flask-JWT-Extended
    jwt = JWTManager(app)

    # Register blueprints with namespaces
    api.add_namespace(admin_bp, path="/admin")
    api.add_namespace(customer_bp, path="/customer")
    api.add_namespace(professional_bp, path="/professional")
    api.add_namespace(service_bp, path="/service")
    api.add_namespace(auth_bp, path="/auth")  # Register the auth blueprint

    return app


from . import models
