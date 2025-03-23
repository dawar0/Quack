import os
from app import create_app
from app.database import db
from app import models
from flask_migrate import Migrate, upgrade, migrate, init, downgrade
import click

app = create_app()
migrate = Migrate(app, db)


@app.cli.command("seed")
@click.option("--drop", is_flag=True, help="Drop all tables before seeding.")
def seed_db(drop):
    """Seeds the database with initial data."""
    if drop:
        with app.app_context():
            db.drop_all()
            db.create_all()
            print("Tables dropped and recreated.")

    print("Seeding database...")

    # Create initial roles (if using multiple roles)
    with app.app_context():
        admin_role = models.Role.query.filter_by(name="admin").first()
        if not admin_role:
            admin_role = models.Role(name="admin")
            db.session.add(admin_role)
            db.session.commit()
            print("Admin role created.")

        professional_role = models.Role.query.filter_by(name="professional").first()
        if not professional_role:
            professional_role = models.Role(name="professional")
            db.session.add(professional_role)
            db.session.commit()
            print("Professional role created.")

        customer_role = models.Role.query.filter_by(name="customer").first()
        if not customer_role:
            customer_role = models.Role(name="customer")
            db.session.add(customer_role)
            db.session.commit()
            print("Customer role created.")

        # Create an initial admin user (if not exists)
        admin_user = models.User.query.filter_by(username="admin").first()
        if not admin_user:
            from werkzeug.security import generate_password_hash

            hashed_password = generate_password_hash(
                "admin"
            )  # Use a strong password in production
            admin_user = models.User(username="admin", password=hashed_password)
            if admin_role:
                admin_user.roles.append(admin_role)
            db.session.add(admin_user)
            db.session.commit()
            print("Admin user created.")

        # Create default service types (if not exist)
        ac_servicing = models.Service.query.filter_by(name="AC Servicing").first()
        if not ac_servicing:
            ac_servicing = models.Service(
                name="AC Servicing",
                price=50.0,
                time_required="2 hours",
                description="Standard AC servicing.",
            )
            db.session.add(ac_servicing)
            db.session.commit()
            print("AC Servicing created.")

        plumbing = models.Service.query.filter_by(name="Plumbing").first()
        if not plumbing:
            plumbing = models.Service(
                name="Plumbing",
                price=40.0,
                time_required="1-3 hours",
                description="General plumbing services.",
            )
            db.session.add(plumbing)
            db.session.commit()
            print("Plumbing created.")

        print("Database seeding complete.")


if __name__ == "__main__":
    # No need for manager.run() with Flask CLI
    pass
