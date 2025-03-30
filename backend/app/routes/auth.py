from flask import Blueprint, request, current_app, send_file, render_template_string
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
from ..tasks.email_tasks import (
    send_welcome_email_task,
    send_account_status_email_task,
    send_newsletter_email_task,
    send_profile_update_email_task,
    send_admin_notification_email_task,
    send_test_email_task,
)
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


# NeoBrutalist email templates
NEOBRUTALIST_HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ subject }}</title>
    <style>
        body {
            font-family: 'Courier New', monospace;
            background-color: #fcf7e6;
            color: #000;
            margin: 0;
            padding: 0;
            line-height: 1.5;
        }
        .container {
            max-width: 600px;
            margin: 20px auto;
            padding: 20px;
            background-color: #fff45c;
            border: 3px solid #000;
            box-shadow: 8px 8px 0 #000;
        }
        h1 {
            font-size: 28px;
            margin-bottom: 25px;
            text-transform: uppercase;
            border-bottom: 5px solid #000;
            padding-bottom: 10px;
            font-weight: 900;
        }
        h1:before, h1:after {
            content: " 🦆 ";
            display: inline;
        }
        .content {
            padding: 20px;
            background-color: #fff;
            border: 2px solid #000;
        }
        p {
            margin-bottom: 15px;
            font-size: 16px;
        }
        .footer {
            margin-top: 30px;
            padding-top: 15px;
            border-top: 3px solid #000;
            font-weight: bold;
            text-align: center;
        }
        .footer:before {
            content: "🦆";
            display: block;
            font-size: 24px;
            margin-bottom: 10px;
        }
        .button {
            display: inline-block;
            padding: 12px 20px;
            background-color: #ff6b6b;
            color: #000;
            text-decoration: none;
            text-transform: uppercase;
            font-weight: bold;
            border: 2px solid #000;
            box-shadow: 4px 4px 0 #000;
            margin: 20px 0;
            transition: all 0.2s;
        }
        .button:hover {
            background-color: #ff8e8e;
            transform: translate(-2px, -2px);
            box-shadow: 6px 6px 0 #000;
        }
        .highlight {
            background-color: #a2ffe9;
            padding: 2px 5px;
            border: 1px solid #000;
        }
        ul {
            list-style-type: square;
            margin-left: 20px;
        }
        li {
            margin-bottom: 10px;
        }
        .duck-icon {
            font-size: 20px;
            vertical-align: middle;
            margin: 0 5px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>{{ title }}</h1>
        <div class="content">
            {{ content|safe }}
        </div>
        <div class="footer">
            {{ footer|safe }}
        </div>
    </div>
</body>
</html>
"""


# Account Status Change Email Route
@auth_bp.route("/account-status-email")
class AccountStatusEmail(Resource):
    @auth_bp.doc(description="Send email when account status changes")
    @admin_required()
    def post(self):
        """Send email notification when account status changes."""
        data = request.get_json()

        if not data:
            return {"message": "No data provided"}, 400

        user_id = data.get("user_id")
        status = data.get("status")
        reason = data.get("reason")

        if not user_id or not status:
            return {"message": "User ID and status are required"}, 400

        user = User.query.get(int(user_id))
        if not user or not user.email:
            return {"message": "User not found or has no email"}, 404

        # Create neobrutalist HTML content
        title = f"Account {status.capitalize()}"

        status_messages = {
            "approved": "Your account has been approved! You can now login and access all professional features.",
            "rejected": f"Your account registration has been rejected. <span class='highlight'>Reason: {reason or 'Not specified'}</span>.",
            "blocked": f"Your account has been blocked. <span class='highlight'>Reason: {reason or 'Not specified'}</span>.",
            "unblocked": "Your account has been unblocked. You can now login and use the platform again.",
        }

        message = status_messages.get(
            status,
            f"Your account status has been changed to: <span class='highlight'>{status}</span>",
        )

        content_html = f"""
            <p>Hello <strong>{user.name or user.username}</strong>, <span class="duck-icon">🦆</span></p>
            <p>{message}</p>
            <p>If you have any questions, please contact our support team.</p>
            <a href="#" class="button">Contact Support <span class="duck-icon">🦆</span></a>
        """

        footer_html = "<p>The Quack Team <span class='duck-icon'>🦆</span></p>"

        html_body = render_template_string(
            NEOBRUTALIST_HTML_TEMPLATE,
            subject=f"Account {status.capitalize()} - Quack",
            title=title,
            content=content_html,
            footer=footer_html,
        )

        # For text emails, we'll use a simpler format
        text_body = f"""
        Hello {user.name or user.username},
        
        {status_messages.get(status, f"Your account status has been changed to: {status}")}
        
        If you have any questions, please contact our support team.
        
        The Quack Team
        """

        # Send the email asynchronously
        send_account_status_email_task.delay(
            user.email, user.name or user.username, status, reason
        )

        return {"message": f"Account status email sent to {user.email}"}, 200


# Newsletter Email Route
@auth_bp.route("/newsletter-email")
class NewsletterEmail(Resource):
    @auth_bp.doc(description="Send newsletter or marketing email")
    @admin_required()
    def post(self):
        """Send newsletter or marketing email to multiple recipients."""
        data = request.get_json()

        if not data:
            return {"message": "No data provided"}, 400

        subject = data.get("subject")
        campaign_name = data.get("campaign_name")
        content = data.get("content")
        recipient_type = data.get(
            "recipient_type", "all"
        )  # all, customers, professionals

        if not subject or not campaign_name or not content:
            return {"message": "Subject, campaign name and content are required"}, 400

        # Get recipients based on type
        recipients = []

        if recipient_type == "customers":
            # Get all customers
            customer_role = Role.query.filter_by(name="customer").first()
            if customer_role:
                customers = User.query.filter(
                    User.roles.contains(customer_role), User.email.isnot(None)
                ).all()
                recipients = [user.email for user in customers if user.email]

        elif recipient_type == "professionals":
            # Get all professionals
            professional_role = Role.query.filter_by(name="professional").first()
            if professional_role:
                professionals = User.query.filter(
                    User.roles.contains(professional_role), User.email.isnot(None)
                ).all()
                recipients = [user.email for user in professionals if user.email]

        else:
            # Get all users with email
            users = User.query.filter(User.email.isnot(None)).all()
            recipients = [user.email for user in users if user.email]

        if not recipients:
            return {"message": "No recipients found"}, 404

        # Create neobrutalist HTML content
        content_html = f"""
            <p><span class="duck-icon">🦆</span> Important announcement from Quack! <span class="duck-icon">🦆</span></p>
            <div>{content}</div>
            <a href="#" class="button">Learn More <span class="duck-icon">🦆</span></a>
            <hr>
            <p><small>You're receiving this because you subscribed to our newsletter.
            <a href="#">Unsubscribe</a></small></p>
        """

        footer_html = "<p>The Quack Team <span class='duck-icon'>🦆</span></p>"

        html_body = render_template_string(
            NEOBRUTALIST_HTML_TEMPLATE,
            subject=subject,
            title=campaign_name,
            content=content_html,
            footer=footer_html,
        )

        # For text emails
        text_body = f"""
        {content}
        
        ---
        You're receiving this because you subscribed to our newsletter.
        To unsubscribe, click here: [unsubscribe link]
        
        The Quack Team
        """

        # Send the email asynchronously
        send_newsletter_email_task.delay(recipients, subject, campaign_name, content)

        return {
            "message": f"Newsletter email sent to {len(recipients)} recipients",
            "recipient_count": len(recipients),
        }, 200


# Profile Update Email Route
@auth_bp.route("/profile-update-email")
class ProfileUpdateEmail(Resource):
    @auth_bp.doc(description="Send email when user profile is updated")
    @jwt_required()
    def post(self):
        """Send notification when a user updates their profile."""
        data = request.get_json()

        if not data:
            return {"message": "No data provided"}, 400

        updated_fields = data.get("updated_fields", [])

        if not updated_fields:
            return {"message": "Updated fields are required"}, 400

        current_user_id = get_jwt_identity()
        user = User.query.get(int(current_user_id))

        if not user or not user.email:
            return {"message": "User not found or has no email"}, 404

        # Format the updated fields for display
        fields_str = ", ".join(updated_fields)
        fields_html = "".join(
            [f"<li><strong>{field}</strong></li>" for field in updated_fields]
        )

        # Create neobrutalist HTML content
        content_html = f"""
            <p>Hello <strong>{user.name or user.username}</strong>, <span class="duck-icon">🦆</span></p>
            <p>Your profile has been successfully updated. The following information was changed:</p>
            <ul>
                {fields_html}
            </ul>
            <p>If you did not make these changes, please contact our support team immediately.</p>
            <a href="#" class="button">Contact Support <span class="duck-icon">🦆</span></a>
        """

        footer_html = "<p>The Quack Team <span class='duck-icon'>🦆</span></p>"

        html_body = render_template_string(
            NEOBRUTALIST_HTML_TEMPLATE,
            subject="Profile Updated - Quack",
            title="Profile Updated",
            content=content_html,
            footer=footer_html,
        )

        # For text emails
        text_body = f"""
        Hello {user.name or user.username},
        
        Your profile has been successfully updated. The following information was changed:
        {fields_str}
        
        If you did not make these changes, please contact our support team immediately.
        
        The Quack Team
        """

        # Send the email asynchronously
        send_profile_update_email_task.delay(
            user.email, user.name or user.username, updated_fields
        )

        return {"message": "Profile update email sent"}, 200


# Admin Notification Email Route
@auth_bp.route("/admin-notification-email")
class AdminNotificationEmail(Resource):
    @auth_bp.doc(description="Send notification to admin about important events")
    def post(self):
        """Send a notification to admin about important events."""
        data = request.get_json()

        if not data:
            return {"message": "No data provided"}, 400

        event_type = data.get("event_type")
        details = data.get("details", {})

        if not event_type:
            return {"message": "Event type is required"}, 400

        # Get admin users with email
        admin_role = Role.query.filter_by(name="admin").first()
        if not admin_role:
            return {"message": "Admin role not found"}, 404

        admins = User.query.filter(
            User.roles.contains(admin_role), User.email.isnot(None)
        ).all()

        admin_emails = [admin.email for admin in admins if admin.email]

        if not admin_emails:
            return {"message": "No admin emails found"}, 404

        # Format details dict into HTML
        details_html = "".join(
            [f"<li><strong>{k}:</strong> {v}</li>" for k, v in details.items()]
        )

        # Create neobrutalist HTML content
        content_html = f"""
            <p><span class="duck-icon">🦆</span> An important event has occurred that requires your attention.</p>
            <h2 class="highlight">Event Details: <span class="duck-icon">🦆</span></h2>
            <ul>
                {details_html}
            </ul>
            <p>This is an automated message from the Quack system.</p>
        """

        footer_html = "<p>Quack Admin System <span class='duck-icon'>🦆</span></p>"

        html_body = render_template_string(
            NEOBRUTALIST_HTML_TEMPLATE,
            subject=f"Admin Notification: {event_type} - Quack",
            title=f"Admin Notification: {event_type}",
            content=content_html,
            footer=footer_html,
        )

        # For text emails
        details_str = "\n".join([f"{k}: {v}" for k, v in details.items()])

        text_body = f"""
        Admin Notification: {event_type}
        
        Event Details:
        {details_str}
        
        This is an automated message from the Quack system.
        """

        # Send the email to each admin
        for admin_email in admin_emails:
            send_admin_notification_email_task.delay(
                admin_email, f"Admin Notification: {event_type}", event_type, details
            )

        return {
            "message": f"Admin notification email sent to {len(admin_emails)} admins",
            "admin_count": len(admin_emails),
        }, 200


# Test Email Route
@auth_bp.route("/test-email")
class TestEmail(Resource):
    template_model = auth_bp.model(
        "EmailTemplate",
        {
            "email": fields.String(
                required=True, description="Recipient email address"
            ),
            "template_type": fields.String(
                required=False,
                description="Type of template to test",
                enum=[
                    "welcome",
                    "notification",
                    "account_status",
                    "newsletter",
                    "profile_update",
                    "admin_notification",
                    "neobrutalist",
                ],
                default="neobrutalist",
            ),
            "data": fields.Raw(
                required=False,
                description="Optional data to populate the template with",
            ),
        },
        model_id="email_template",
    )

    @auth_bp.doc(
        description="Send a test email with selected template to verify email configuration and preview design",
        params={
            "email": "Email address to send the test email to",
            "template_type": "Type of template to test (welcome, notification, account_status, newsletter, profile_update, admin_notification, neobrutalist)",
            "data": "Optional data to populate the template with",
        },
        responses={
            200: "Test email sent successfully",
            400: "Invalid input data",
        },
    )
    @auth_bp.expect(template_model)
    @admin_required()
    def post(self):
        """
        Send a test email to verify email configuration is working.

        Choose which template to test:
        - welcome: Welcome email for new users
        - notification: General notification email
        - account_status: Account status change notification
        - newsletter: Marketing/newsletter email
        - profile_update: Profile update confirmation
        - admin_notification: Admin alerts
        - neobrutalist: Full demonstration of neobrutalist design (default)

        The test email includes rich dummy data to showcase template features.
        """
        data = request.get_json()

        if not data:
            return {"message": "No data provided"}, 400

        email = data.get("email")
        template_type = data.get("template_type", "neobrutalist")
        template_data = data.get("data", {})

        if not email:
            return {"message": "Email address is required"}, 400

        # Default template is the neobrutalist showcase
        if template_type == "neobrutalist" or not template_type:
            # Send the standard test email with dummy data
            send_test_email_task.delay(email)
            template_name = "neobrutalist showcase"

        # Welcome email template
        elif template_type == "welcome":
            user_name = template_data.get("name", "Test User")
            send_welcome_email_task.delay(email, user_name)
            template_name = "welcome"

        # Notification email template
        elif template_type == "notification":
            user_name = template_data.get("name", "Test User")
            subject = template_data.get("subject", "Important Notification")
            message = template_data.get(
                "message", "This is a test notification message from Quack."
            )
            send_notification_email_task.delay(subject, email, user_name, message)
            template_name = "notification"

        # Account status email template
        elif template_type == "account_status":
            user_name = template_data.get("name", "Test User")
            status = template_data.get("status", "approved")
            reason = template_data.get("reason", "Test reason")
            send_account_status_email_task.delay(email, user_name, status, reason)
            template_name = f"account status ({status})"

        # Newsletter email template
        elif template_type == "newsletter":
            subject = template_data.get("subject", "Quack Newsletter")
            campaign_name = template_data.get("campaign_name", "Test Campaign")
            content = template_data.get(
                "content",
                "<p>This is a test newsletter content. It could contain <strong>formatted text</strong>, images, and links.</p>",
            )
            send_newsletter_email_task.delay([email], subject, campaign_name, content)
            template_name = "newsletter"

        # Profile update email template
        elif template_type == "profile_update":
            user_name = template_data.get("name", "Test User")
            updated_fields = template_data.get(
                "updated_fields", ["name", "email", "address", "phone"]
            )
            send_profile_update_email_task.delay(email, user_name, updated_fields)
            template_name = "profile update"

        # Admin notification email template
        elif template_type == "admin_notification":
            event_type = template_data.get(
                "event_type", "New Professional Registration"
            )
            subject = template_data.get("subject", f"Admin Notification: {event_type}")
            details = template_data.get(
                "details",
                {
                    "user_id": "12345",
                    "username": "new_professional",
                    "email": "professional@example.com",
                    "timestamp": "2023-08-22 14:30:45",
                    "action_required": "Review profile and documents",
                },
            )
            send_admin_notification_email_task.delay(
                email, subject, event_type, details
            )
            template_name = "admin notification"

        else:
            return {"message": f"Unknown template type: {template_type}"}, 400

        return {
            "message": f"Test email ({template_name} template) sent to {email}",
            "details": "The email contains dummy data to showcase the template design",
            "template": template_type,
        }, 200

    @auth_bp.doc(
        description="Check email configuration status",
        responses={200: "Email configuration status retrieved successfully"},
    )
    @admin_required()
    def get(self):
        """
        Check if email configuration is properly set up.

        Verifies all required email configuration parameters are present in the application
        config, including mail server, port, credentials, and default sender.
        """
        from ..email import check_email_config

        config_status = check_email_config()

        if config_status["is_configured"]:
            return {
                "message": "Email configuration is properly set up",
                "status": "configured",
                "config": config_status["config"],
                "templates": {
                    "welcome": "Welcome email for new users",
                    "notification": "General notification email",
                    "account_status": "Account status change notification (approved, rejected, blocked, unblocked)",
                    "newsletter": "Marketing/newsletter email",
                    "profile_update": "Profile update confirmation",
                    "admin_notification": "Admin alerts",
                    "neobrutalist": "Full demonstration of neobrutalist design",
                },
            }, 200
        else:
            return {
                "message": "Email configuration is incomplete",
                "status": "incomplete",
                "config": config_status["config"],
                "missing": [
                    key
                    for key, value in config_status["config"].items()
                    if value is None or value is False
                ],
                "help": "Use the POST method to test sending an email once configuration is complete",
            }, 200
