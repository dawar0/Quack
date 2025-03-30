from faker import Faker
from datetime import datetime, timedelta
import random
from werkzeug.security import generate_password_hash
from app.models import User, Role, Service, ServiceRequest
from sqlalchemy.orm import Session

fake = Faker(["en_IN"])  # Using Indian locale for more realistic data


class UserFactory:
    @staticmethod
    def create_admin(session: Session):
        with session.no_autoflush:
            admin_role = session.query(Role).filter_by(name="admin").first()
            return User(
                username="admin",
                password=generate_password_hash("admin"),
                name="Admin User",
                email="admin@example.com",
                phone_number=fake.phone_number(),
                roles=[admin_role],
            )

    @staticmethod
    def create_professional(session: Session, service_type):
        first_name = fake.first_name()
        last_name = fake.last_name()
        username = fake.user_name()

        # Ensure username is unique
        with session.no_autoflush:
            while session.query(User).filter_by(username=username).first():
                username = fake.user_name()

            professional_role = (
                session.query(Role).filter_by(name="professional").first()
            )
            return User(
                username=username,
                password=generate_password_hash("password123"),
                name=f"{first_name} {last_name}",
                email=fake.email(),
                phone_number=fake.phone_number(),
                roles=[professional_role],
                service_type=service_type,
                experience=f"{random.randint(1, 10)} years",
                profile_docs_verified=random.choice([True, False]),
                blocked=False,
                description=fake.text(max_nb_chars=200),
            )

    @staticmethod
    def create_customer(session: Session):
        first_name = fake.first_name()
        last_name = fake.last_name()
        username = fake.user_name()

        # Ensure username is unique
        with session.no_autoflush:
            while session.query(User).filter_by(username=username).first():
                username = fake.user_name()

            customer_role = session.query(Role).filter_by(name="customer").first()
            return User(
                username=username,
                password=generate_password_hash("password123"),
                name=f"{first_name} {last_name}",
                email=fake.email(),
                phone_number=fake.phone_number(),
                roles=[customer_role],
                profile_docs_verified=True,
                blocked=False,
            )


class ServiceFactory:
    @staticmethod
    def create_services():
        return [
            Service(
                name="AC Servicing",
                price=50.0,
                time_required="2 hours",
                description="Professional AC cleaning and maintenance service.",
            ),
            Service(
                name="Plumbing",
                price=40.0,
                time_required="1-3 hours",
                description="Expert plumbing repair and installation services.",
            ),
            Service(
                name="Electrical",
                price=45.0,
                time_required="1-2 hours",
                description="Complete electrical repair and maintenance.",
            ),
            Service(
                name="Carpenter",
                price=35.0,
                time_required="2-4 hours",
                description="Professional carpentry and woodwork services.",
            ),
            Service(
                name="Painter",
                price=30.0,
                time_required="4-6 hours",
                description="Interior and exterior painting services.",
            ),
            Service(
                name="Appliance Repair",
                price=55.0,
                time_required="1-2 hours",
                description="Repair services for home appliances.",
            ),
            Service(
                name="Pest Control",
                price=60.0,
                time_required="1 hour",
                description="Effective pest control and prevention.",
            ),
            Service(
                name="House Cleaning",
                price=25.0,
                time_required="2-3 hours",
                description="Professional house cleaning services.",
            ),
        ]


class ServiceRequestFactory:
    @staticmethod
    def create_service_request(customer, service, professional=None):
        status = random.choice(["Pending", "Accepted", "Completed", "Cancelled"])
        request_date = datetime.now() - timedelta(days=random.randint(0, 30))
        completion_date = None
        if status == "Completed":
            completion_date = request_date + timedelta(days=random.randint(1, 5))

        return ServiceRequest(
            customer_id=customer.id,
            service_id=service.id,
            professional_id=professional.id if professional else None,
            date_of_request=request_date,
            date_of_completion=completion_date,
            service_status=status,
            remarks=fake.text(max_nb_chars=100),
            location_pin_code=fake.postcode(),
            preferred_date=request_date + timedelta(days=random.randint(1, 7)),
        )
