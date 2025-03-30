from typing import List, Optional
from app.celery_utils import celery_app
from app import create_app
from app.utils.email import send_email


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
    text_body = f"""
    Hello {user_name},
    
    Welcome to Quack! We're excited to have you on board.
    
    Thank you for joining our platform. If you have any questions, 
    please don't hesitate to contact us.
    
    The Quack Team
    """
    html_body = f"""
    <h1>Welcome to Quack!</h1>
    <p>Hello {user_name},</p>
    <p>Welcome to Quack! We're excited to have you on board.</p>
    <p>Thank you for joining our platform. If you have any questions, 
    please don't hesitate to contact us.</p>
    <p>The Quack Team</p>
    """

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
    text_body = f"""
    Hello {user_name},
    
    {message}
    
    The Quack Team
    """
    html_body = f"""
    <p>Hello {user_name},</p>
    <p>{message}</p>
    <p>The Quack Team</p>
    """

    return send_email_task.delay(
        subject=subject,
        recipients=[user_email],
        text_body=text_body,
        html_body=html_body,
    )
