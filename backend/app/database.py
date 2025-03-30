from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
Model = db.Model


def init_app(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
        # Initialize roles if they don't exist
        from .models import Role  # Import here to avoid circular import

        roles = ["admin", "professional", "customer"]
        for role_name in roles:
            role = Role.query.filter_by(name=role_name).first()
            if not role:
                role = Role(name=role_name)
                db.session.add(role)
        db.session.commit()
