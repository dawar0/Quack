from typing import List, Optional
from app.celery_utils import celery_app
from app.utils.email import send_email
from flask import render_template_string


# Neobrutalist HTML template for all emails
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


@celery_app.task(bind=True)
def send_email_task(
    self,
    subject: str,
    recipients: List[str],
    text_body: str,
    html_body: Optional[str] = None,
    sender: Optional[str] = None,
    cc: Optional[List[str]] = None,
    bcc: Optional[List[str]] = None,
):
    """
    Celery task to send an email asynchronously.

    Args:
        subject: Email subject
        recipients: List of recipient email addresses
        text_body: Plain text content of the email
        html_body: HTML content of the email (optional)
        sender: Sender email address (optional)
        cc: List of CC email addresses (optional)
        bcc: List of BCC email addresses (optional)

    Returns:
        str: Success message
    """
    from app import create_app

    app = create_app()
    with app.app_context():
        send_email(
            subject=subject,
            recipients=recipients,
            text_body=text_body,
            html_body=html_body,
            sender=sender,
            cc=cc,
            bcc=bcc,
        )
        return f"Email sent to {', '.join(recipients)}"


@celery_app.task(bind=True)
def send_welcome_email_task(self, user_email: str, user_name: str):
    """
    Send a welcome email to a new user.

    Args:
        user_email: The user's email address
        user_name: The user's name

    Returns:
        str: Success message
    """
    subject = "Welcome to Quack!"

    # Text version
    text_body = f"""
    Hello {user_name},
    
    Welcome to Quack! We're excited to have you on board.
    
    Thank you for joining our platform. If you have any questions, 
    please don't hesitate to contact us.
    
    The Quack Team
    """

    # HTML content using neobrutalist style
    content_html = f"""
        <p>Hello <strong>{user_name}</strong>, <span class="duck-icon">🦆</span></p>
        <p>Welcome to Quack! We're excited to have you on board.</p>
        <p>Thank you for joining our platform. If you have any questions, 
        please don't hesitate to contact us.</p>
        <a href="#" class="button">Get Started <span class="duck-icon">🦆</span></a>
    """

    footer_html = "<p>The Quack Team <span class='duck-icon'>🦆</span></p>"

    # Generate HTML using template
    from app import create_app

    app = create_app()
    with app.app_context():
        html_body = render_template_string(
            NEOBRUTALIST_HTML_TEMPLATE,
            subject=subject,
            title="Welcome to Quack!",
            content=content_html,
            footer=footer_html,
        )

    return send_email_task.delay(
        subject=subject,
        recipients=[user_email],
        text_body=text_body,
        html_body=html_body,
    )


@celery_app.task(bind=True)
def send_notification_email_task(
    self, subject: str, user_email: str, user_name: str, message: str
):
    """
    Send a notification email to a user.

    Args:
        subject: Email subject
        user_email: The user's email address
        user_name: The user's name
        message: The notification message

    Returns:
        str: Success message
    """
    # Text version
    text_body = f"""
    Hello {user_name},
    
    {message}
    
    The Quack Team
    """

    # HTML content using neobrutalist style
    content_html = f"""
        <p>Hello <strong>{user_name}</strong>, <span class="duck-icon">🦆</span></p>
        <p>{message}</p>
    """

    footer_html = "<p>The Quack Team <span class='duck-icon'>🦆</span></p>"

    # Generate HTML using template
    from app import create_app

    app = create_app()
    with app.app_context():
        html_body = render_template_string(
            NEOBRUTALIST_HTML_TEMPLATE,
            subject=subject,
            title=subject,
            content=content_html,
            footer=footer_html,
        )

    return send_email_task.delay(
        subject=subject,
        recipients=[user_email],
        text_body=text_body,
        html_body=html_body,
    )


@celery_app.task(bind=True)
def send_account_status_email_task(
    self, user_email: str, user_name: str, status: str, reason: str = None
):
    """
    Send an email when a user's account status changes.

    Args:
        user_email: The user's email address
        user_name: The user's name
        status: The new account status (approved, rejected, blocked, unblocked)
        reason: Reason for status change (optional)

    Returns:
        str: Success message
    """
    status_messages = {
        "approved": "Your account has been approved! You can now login and access all professional features.",
        "rejected": f"Your account registration has been rejected. Reason: {reason or 'Not specified'}.",
        "blocked": f"Your account has been blocked. Reason: {reason or 'Not specified'}.",
        "unblocked": "Your account has been unblocked. You can now login and use the platform again.",
    }

    text_message = status_messages.get(
        status, f"Your account status has been changed to: {status}"
    )
    html_message = status_messages.get(
        status,
        f"Your account status has been changed to: <span class='highlight'>{status}</span>",
    )

    if status in ["rejected", "blocked"] and reason:
        html_message = html_message.replace(
            f"Reason: {reason}", f"Reason: <span class='highlight'>{reason}</span>"
        )

    subject = f"Account {status.capitalize()} - Quack"

    # Text version
    text_body = f"""
    Hello {user_name},
    
    {text_message}
    
    If you have any questions, please contact our support team.
    
    The Quack Team
    """

    # HTML content using neobrutalist style
    content_html = f"""
        <p>Hello <strong>{user_name}</strong>, <span class="duck-icon">🦆</span></p>
        <p>{html_message}</p>
        <p>If you have any questions, please contact our support team.</p>
        <a href="#" class="button">Contact Support <span class="duck-icon">🦆</span></a>
    """

    footer_html = "<p>The Quack Team <span class='duck-icon'>🦆</span></p>"

    # Generate HTML using template
    from app import create_app

    app = create_app()
    with app.app_context():
        html_body = render_template_string(
            NEOBRUTALIST_HTML_TEMPLATE,
            subject=subject,
            title=f"Account {status.capitalize()}",
            content=content_html,
            footer=footer_html,
        )

    return send_email_task.delay(
        subject=subject,
        recipients=[user_email],
        text_body=text_body,
        html_body=html_body,
    )


@celery_app.task(bind=True)
def send_newsletter_email_task(
    self, recipients: List[str], subject: str, campaign_name: str, content: str
):
    """
    Send a newsletter or marketing email to multiple recipients.

    Args:
        recipients: List of recipient email addresses
        subject: Email subject
        campaign_name: Name of the marketing campaign
        content: Content of the newsletter

    Returns:
        str: Success message
    """
    # Text version
    text_body = f"""
    {content}
    
    ---
    You're receiving this because you subscribed to our newsletter.
    To unsubscribe, click here: [unsubscribe link]
    
    The Quack Team
    """

    # HTML content using neobrutalist style
    content_html = f"""
        <p><span class="duck-icon">🦆</span> Important announcement from Quack! <span class="duck-icon">🦆</span></p>
        <div>{content}</div>
        <a href="#" class="button">Learn More <span class="duck-icon">🦆</span></a>
        <hr>
        <p><small>You're receiving this because you subscribed to our newsletter.
        <a href="#">Unsubscribe</a></small></p>
    """

    footer_html = "<p>The Quack Team <span class='duck-icon'>🦆</span></p>"

    # Generate HTML using template
    from app import create_app

    app = create_app()
    with app.app_context():
        html_body = render_template_string(
            NEOBRUTALIST_HTML_TEMPLATE,
            subject=subject,
            title=campaign_name,
            content=content_html,
            footer=footer_html,
        )

    return send_email_task.delay(
        subject=subject,
        recipients=recipients,
        text_body=text_body,
        html_body=html_body,
    )


@celery_app.task(bind=True)
def send_profile_update_email_task(
    self, user_email: str, user_name: str, updated_fields: List[str]
):
    """
    Send a notification when a user updates their profile.

    Args:
        user_email: The user's email address
        user_name: The user's name
        updated_fields: List of fields that were updated

    Returns:
        str: Success message
    """
    fields_str = ", ".join(updated_fields)
    fields_html = "".join(
        [f"<li><strong>{field}</strong></li>" for field in updated_fields]
    )

    subject = "Profile Updated - Quack"

    # Text version
    text_body = f"""
    Hello {user_name},
    
    Your profile has been successfully updated. The following information was changed:
    {fields_str}
    
    If you did not make these changes, please contact our support team immediately.
    
    The Quack Team
    """

    # HTML content using neobrutalist style
    content_html = f"""
        <p>Hello <strong>{user_name}</strong>, <span class="duck-icon">🦆</span></p>
        <p>Your profile has been successfully updated. The following information was changed:</p>
        <ul>
            {fields_html}
        </ul>
        <p>If you did not make these changes, please contact our support team immediately.</p>
        <a href="#" class="button">Contact Support <span class="duck-icon">🦆</span></a>
    """

    footer_html = "<p>The Quack Team <span class='duck-icon'>🦆</span></p>"

    # Generate HTML using template
    from app import create_app

    app = create_app()
    with app.app_context():
        html_body = render_template_string(
            NEOBRUTALIST_HTML_TEMPLATE,
            subject=subject,
            title="Profile Updated",
            content=content_html,
            footer=footer_html,
        )

    return send_email_task.delay(
        subject=subject,
        recipients=[user_email],
        text_body=text_body,
        html_body=html_body,
    )


@celery_app.task(bind=True)
def send_admin_notification_email_task(
    self, admin_email: str, subject: str, event_type: str, details: dict
):
    """
    Send a notification to admin about important events.

    Args:
        admin_email: The admin's email address
        subject: Email subject
        event_type: Type of event (new_professional, document_upload, etc.)
        details: Dictionary with event details

    Returns:
        str: Success message
    """
    # Format details dict into a readable string for text email
    details_str = "\n".join([f"{k}: {v}" for k, v in details.items()])

    # Format details dict into HTML for HTML email
    details_html = "".join(
        [f"<li><strong>{k}:</strong> {v}</li>" for k, v in details.items()]
    )

    # Text version
    text_body = f"""
    Admin Notification: {event_type}
    
    Event Details:
    {details_str}
    
    This is an automated message from the Quack system.
    """

    # HTML content using neobrutalist style
    content_html = f"""
        <p><span class="duck-icon">🦆</span> An important event has occurred that requires your attention.</p>
        <h2 class="highlight">Event Details: <span class="duck-icon">🦆</span></h2>
        <ul>
            {details_html}
        </ul>
        <p>This is an automated message from the Quack system.</p>
    """

    footer_html = "<p>Quack Admin System <span class='duck-icon'>🦆</span></p>"

    # Generate HTML using template
    from app import create_app

    app = create_app()
    with app.app_context():
        html_body = render_template_string(
            NEOBRUTALIST_HTML_TEMPLATE,
            subject=subject,
            title=f"Admin Notification: {event_type}",
            content=content_html,
            footer=footer_html,
        )

    return send_email_task.delay(
        subject=subject,
        recipients=[admin_email],
        text_body=text_body,
        html_body=html_body,
    )


@celery_app.task(bind=True)
def send_test_email_task(self, email: str):
    """
    Send a test email to verify email configuration works.
    Includes rich dummy data to showcase all template features.

    Args:
        email: The recipient's email address

    Returns:
        str: Success message
    """
    subject = "Quack Email Test - Neobrutalist Design"

    # Text version
    text_body = """
    Hello Quack User,
    
    This is a test email from Quack to verify that email functionality is working correctly.
    
    === DUMMY DATA FOR TESTING ===
    
    User Profile:
    - Username: quack_test_user
    - Email: test@quack.com
    - Role: Professional
    - Status: Approved
    
    Recent Activity:
    - 3 new messages
    - 2 pending service requests
    - 1 approved document
    
    If you received this email, your email configuration is set up correctly.
    
    The Quack Team 🦆
    """

    # HTML content with extreme neobrutalist styling
    content_html = """
        <div style="border-left: 10px solid #ff6b6b; padding-left: 15px; margin-bottom: 25px; transform: rotate(-1deg);">
            <p style="font-size: 20px; font-weight: bold;">Hello there, <span class="duck-icon">🦆</span></p>
            <p>This is a <strong>test email</strong> from Quack to verify that email functionality is working correctly.</p>
            <p class="highlight" style="transform: rotate(1deg); display: inline-block; padding: 10px; font-weight: bold; font-size: 18px;">
                If you received this email, your email configuration is set up correctly! <span class="duck-icon">🦆</span>
            </p>
        </div>
        
        <h2 style="margin-top:40px; transform: rotate(-1deg); background-color: #fff45c; display: inline-block; padding: 10px 15px; border: 3px solid #000; box-shadow: 5px 5px 0 #000;">DUMMY DATA PREVIEW <span class="duck-icon">🦆</span></h2>
        
        <div style="background-color: #fffae0; border: 3px solid #000; padding: 20px; margin: 20px 0; box-shadow: 8px 8px 0 #000; position: relative;">
            <!-- Corner ribbon -->
            <div style="position: absolute; top: -10px; right: -10px; background-color: #ff6b6b; color: #000; padding: 10px; border: 2px solid #000; transform: rotate(5deg); font-weight: bold; box-shadow: 3px 3px 0 #000;">
                QUACK!
            </div>
            
            <h3 style="margin-top: 0; border-bottom: 3px solid #000; display: inline-block; padding-bottom: 5px; text-transform: uppercase;">User Profile</h3>
            <ul style="list-style-type: none; padding-left: 0;">
                <li style="margin-bottom: 10px; border-left: 5px solid #ff6b6b; padding-left: 10px;"><strong>Username:</strong> quack_test_user</li>
                <li style="margin-bottom: 10px; border-left: 5px solid #a2ffe9; padding-left: 10px;"><strong>Email:</strong> test@quack.com</li>
                <li style="margin-bottom: 10px; border-left: 5px solid #fff45c; padding-left: 10px;"><strong>Role:</strong> <span class="highlight">Professional</span></li>
                <li style="margin-bottom: 10px; border-left: 5px solid #ff6b6b; padding-left: 10px;"><strong>Status:</strong> <span class="highlight">Approved</span></li>
            </ul>
            
            <h3 style="border-bottom: 3px solid #000; display: inline-block; padding-bottom: 5px; text-transform: uppercase;">Recent Activity</h3>
            <div style="display: flex; flex-wrap: wrap; gap: 10px; margin: 15px 0;">
                <div style="background-color: #ff6b6b; border: 2px solid #000; padding: 10px; flex: 1; min-width: 100px; box-shadow: 4px 4px 0 #000; text-align: center;">
                    <div style="font-size: 24px; font-weight: bold;">3</div>
                    <div>NEW MESSAGES</div>
                </div>
                <div style="background-color: #fff45c; border: 2px solid #000; padding: 10px; flex: 1; min-width: 100px; box-shadow: 4px 4px 0 #000; text-align: center;">
                    <div style="font-size: 24px; font-weight: bold;">2</div>
                    <div>PENDING REQUESTS</div>
                </div>
                <div style="background-color: #a2ffe9; border: 2px solid #000; padding: 10px; flex: 1; min-width: 100px; box-shadow: 4px 4px 0 #000; text-align: center;">
                    <div style="font-size: 24px; font-weight: bold;">1</div>
                    <div>APPROVED DOC</div>
                </div>
            </div>
            
            <h3 style="border-bottom: 3px solid #000; display: inline-block; padding-bottom: 5px; text-transform: uppercase;">Account Details</h3>
            <table style="width: 100%; border-collapse: separate; border-spacing: 0; margin: 15px 0; border: 3px solid #000; box-shadow: 5px 5px 0 #000;">
                <tr style="background-color: #fff45c;">
                    <th style="padding: 12px; text-align: left; border: 2px solid #000; text-transform: uppercase;">Field</th>
                    <th style="padding: 12px; text-align: left; border: 2px solid #000; text-transform: uppercase;">Value</th>
                </tr>
                <tr style="border-bottom: 2px solid #000; background-color: #fff;">
                    <td style="padding: 12px; border: 2px solid #000; font-weight: bold;">Member Since</td>
                    <td style="padding: 12px; border: 2px solid #000;">January 15, 2023</td>
                </tr>
                <tr style="border-bottom: 2px solid #000; background-color: #fff;">
                    <td style="padding: 12px; border: 2px solid #000; font-weight: bold;">Last Login</td>
                    <td style="padding: 12px; border: 2px solid #000;">Today at 2:30 PM</td>
                </tr>
                <tr style="background-color: #fff;">
                    <td style="padding: 12px; border: 2px solid #000; font-weight: bold;">Subscription</td>
                    <td style="padding: 12px; border: 2px solid #000;">
                        <span style="background-color: #ff6b6b; padding: 5px 10px; border: 1px solid #000; font-weight: bold;">PREMIUM</span>
                    </td>
                </tr>
            </table>
        </div>
        
        <p>Check out our <span class="highlight" style="font-weight: bold;">EXTREME NEOBRUTALIST</span> design with bold borders, bright colors, and chunky elements!</p>
        
        <div style="display: flex; flex-direction: column; gap: 15px; margin: 25px 0;">
            <a href="#" class="button" style="transform: rotate(-1deg); font-size: 16px; text-align: center;">VIEW DASHBOARD <span class="duck-icon">🦆</span></a>
            <a href="#" class="button" style="background-color: #a2ffe9; transform: rotate(1deg); font-size: 16px; text-align: center;">VIEW PROFILE <span class="duck-icon">🦆</span></a>
            <a href="#" class="button" style="background-color: #fff45c; transform: rotate(-1deg); font-size: 16px; text-align: center;">ACCOUNT SETTINGS <span class="duck-icon">🦆</span></a>
        </div>
        
        <div style="margin-top: 30px; border: 3px dashed #000; padding: 15px; text-align: center; background-color: #fff45c;">
            <p style="font-weight: bold; margin: 0; font-size: 18px;">🦆 QUACK! QUACK! QUACK! 🦆</p>
        </div>
    """

    footer_html = """
    <p style="font-size: 18px; font-weight: bold;">The Quack Team <span class='duck-icon'>🦆</span></p>
    <div style="background-color: #a2ffe9; padding: 8px; border: 1px solid #000; display: inline-block; transform: rotate(-1deg); margin-top: 10px;">
        <p style="margin: 0; font-size: 12px;">This is a system generated test email. Please do not reply.</p>
    </div>
    """

    # Generate HTML using template
    from app import create_app

    app = create_app()
    with app.app_context():
        html_body = render_template_string(
            NEOBRUTALIST_HTML_TEMPLATE,
            subject=subject,
            title="NEOBRUTALIST EMAIL TEST",
            content=content_html,
            footer=footer_html,
        )

    return send_email_task.delay(
        subject=subject,
        recipients=[email],
        text_body=text_body,
        html_body=html_body,
    )
