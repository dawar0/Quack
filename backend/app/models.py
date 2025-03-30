from .database import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.Text)
    experience = db.Column(db.String(100))
    service_type = db.Column(db.String(100))
    profile_docs_verified = db.Column(db.Boolean, default=False)
    blocked = db.Column(db.Boolean, default=False)
    status = db.Column(
        db.String(20), default="pending"
    )  # pending, approved, disapproved
    rejection_reason = db.Column(db.Text)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    phone_number = db.Column(db.String(20))
    profile_image = db.Column(db.String(255))
    address = db.Column(db.String(255))
    customer_requests = db.relationship(
        "ServiceRequest",
        foreign_keys="ServiceRequest.customer_id",
        backref="customer_user",
        lazy=True,
    )
    professional_requests = db.relationship(
        "ServiceRequest",
        foreign_keys="ServiceRequest.professional_id",
        backref="professional_user",
        lazy=True,
    )
    roles = db.relationship("Role", secondary="user_roles", backref="users", lazy=True)

    @property
    def role_ids(self):
        return [role.id for role in self.roles]

    def __repr__(self):
        return f"<User {self.username}>"


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)

    def __repr__(self):
        return f"<Role {self.name}>"


class UserRoles(db.Model):
    __tablename__ = "user_roles"
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"), primary_key=True)


class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    time_required = db.Column(db.String(50))
    description = db.Column(db.Text)

    requests = db.relationship("ServiceRequest", backref="service", lazy=True)

    def __repr__(self):
        return f"<Service {self.name}>"


class ServiceRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey("service.id"), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    professional_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    date_of_request = db.Column(db.DateTime, default=datetime.utcnow)
    date_of_completion = db.Column(db.DateTime)
    service_status = db.Column(db.String(20), default="pending")
    remarks = db.Column(db.Text)
    location_pin_code = db.Column(db.String(10))
    preferred_date = db.Column(db.Date)
    customer = db.relationship(
        "User",
        foreign_keys=[customer_id],
    )
    professional = db.relationship(
        "User",
        foreign_keys=[professional_id],
    )

    def __repr__(self):
        return f"<ServiceRequest {self.id}>"


class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    document_type = db.Column(
        db.String(50), nullable=False
    )  # e.g., 'id_proof', 'certification', 'insurance'
    file_name = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    verified = db.Column(db.Boolean, default=False)
    rejected = db.Column(db.Boolean, default=False)
    rejection_reason = db.Column(db.Text)

    # Relationship with User
    user = db.relationship("User", backref=db.backref("documents", lazy=True))

    def __repr__(self):
        return f"<Document {self.document_type} for User {self.user_id}>"
