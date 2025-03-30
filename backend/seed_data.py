from datetime import datetime, timedelta
import random
from werkzeug.security import generate_password_hash
from app import create_app, db
from app.models import User, Role, Service, ServiceRequest
from factories import UserFactory, ServiceFactory, ServiceRequestFactory


def seed_database():
    app = create_app()
    with app.app_context():
        # Drop all tables and recreate them
        db.drop_all()
        db.create_all()
        print("Tables dropped and recreated.")

        # Create roles
        admin_role = Role(name="admin")
        professional_role = Role(name="professional")
        customer_role = Role(name="customer")
        db.session.add_all([admin_role, professional_role, customer_role])
        db.session.commit()
        print("Roles created.")

        # Create admin user
        admin_user = UserFactory.create_admin(db.session)
        db.session.add(admin_user)
        db.session.commit()
        print("Admin user created.")

        # Create services
        services = ServiceFactory.create_services()
        db.session.add_all(services)
        db.session.commit()
        print("Services created.")

        # Create professionals
        professional_types = [service.name for service in services]
        professionals = []
        for _ in range(20):  # Create 20 professionals
            service_type = random.choice(professional_types)
            professional = UserFactory.create_professional(db.session, service_type)
            professionals.append(professional)
        db.session.add_all(professionals)
        db.session.commit()
        print("Professionals created.")

        # Create customers
        customers = []
        for _ in range(50):  # Create 50 customers
            customer = UserFactory.create_customer(db.session)
            customers.append(customer)
        db.session.add_all(customers)
        db.session.commit()
        print("Customers created.")

        # Create service requests
        service_requests = []
        for _ in range(100):  # Create 100 service requests
            customer = random.choice(customers)
            service = random.choice(services)
            professional = (
                random.choice(professionals) if random.random() < 0.7 else None
            )
            service_request = ServiceRequestFactory.create_service_request(
                customer, service, professional
            )
            service_requests.append(service_request)
        db.session.add_all(service_requests)
        db.session.commit()
        print("Service requests created.")

        print("Database seeding completed successfully!")


if __name__ == "__main__":
    seed_database()
