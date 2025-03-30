from typing import List, Optional
from flask import current_app
from flask_mail import Message, Mail

mail = Mail()


def init_mail(app):
    """Initialize the mail extension with the Flask app."""
    mail.init_app(app)


def send_email(
    subject: str,
    recipients: List[str],
    text_body: str,
    html_body: Optional[str] = None,
    sender: Optional[str] = None,
    cc: Optional[List[str]] = None,
    bcc: Optional[List[str]] = None,
    attachments: Optional[List[tuple]] = None,
):
    """
    Send an email with the application's configured mail settings.

    Args:
        subject: Email subject
        recipients: List of recipient email addresses
        text_body: Plain text content of the email
        html_body: HTML content of the email (optional)
        sender: Sender email address (optional, defaults to MAIL_DEFAULT_SENDER)
        cc: List of CC email addresses (optional)
        bcc: List of BCC email addresses (optional)
        attachments: List of attachments as tuples (filename, media_type, data) (optional)

    Returns:
        None
    """
    msg = Message(
        subject=subject,
        recipients=recipients,
        body=text_body,
        html=html_body,
        sender=sender or current_app.config["MAIL_DEFAULT_SENDER"],
        cc=cc,
        bcc=bcc,
    )

    # Add attachments if provided
    if attachments:
        for attachment in attachments:
            filename, media_type, data = attachment
            msg.attach(filename, media_type, data)

    mail.send(msg)
