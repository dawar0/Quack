import click
from flask.cli import with_appcontext
from ..tasks.email_tasks import (
    send_welcome_email_task,
    send_notification_email_task,
    send_account_status_email_task,
    send_newsletter_email_task,
    send_profile_update_email_task,
    send_admin_notification_email_task,
    send_test_email_task,
)
from ..email import check_email_config
import json
import os


def register_email_commands(app):
    """Register email-related CLI commands with the application."""
    app.cli.add_command(test_email_cmd)
    app.cli.add_command(check_email_config_cmd)
    app.cli.add_command(list_email_templates_cmd)


@click.command("test-email")
@click.argument("email")
@click.option(
    "--template",
    "-t",
    default="neobrutalist",
    type=click.Choice(
        [
            "welcome",
            "notification",
            "account_status",
            "newsletter",
            "profile_update",
            "admin_notification",
            "neobrutalist",
        ]
    ),
    help="Email template to test",
)
@click.option(
    "--data",
    "-d",
    help="JSON string or path to JSON file with template data",
)
@click.option(
    "--sync",
    "-s",
    is_flag=True,
    default=False,
    help="Send email synchronously (bypass Celery/Redis)",
)
@with_appcontext
def test_email_cmd(email, template, data, sync):
    """
    Send a test email with selected template.

    Examples:

    \b
    # Send default neobrutalist test email
    flask test-email user@example.com

    \b
    # Send welcome email
    flask test-email user@example.com -t welcome

    \b
    # Send notification with custom data
    flask test-email user@example.com -t notification -d '{"name": "John", "subject": "Hello", "message": "Custom message"}'

    \b
    # Send template with data from file
    flask test-email user@example.com -t newsletter -d ./data.json

    \b
    # Send email synchronously (without Celery/Redis)
    flask test-email user@example.com --sync
    """
    template_data = {}

    # Process data if provided
    if data:
        # Check if it's a file path
        if os.path.exists(data):
            try:
                with open(data, "r") as f:
                    template_data = json.load(f)
                click.echo(f"Loaded data from file: {data}")
            except json.JSONDecodeError:
                click.echo(f"Error: {data} is not a valid JSON file", err=True)
                return
            except Exception as e:
                click.echo(f"Error loading file: {str(e)}", err=True)
                return
        else:
            # Try to parse as JSON string
            try:
                template_data = json.loads(data)
            except json.JSONDecodeError:
                click.echo("Error: Invalid JSON data", err=True)
                return

    click.echo(f"Sending {template} test email to {email}...")

    # Direct imports for sync mode
    if sync:
        from flask import render_template_string
        from ..utils.email import send_email
        from ..email import NEOBRUTALIST_HTML_TEMPLATE

    try:
        # Call appropriate task based on template type
        if template == "welcome":
            user_name = template_data.get("name", "Test User")
            if sync:
                # Use the template from email module, not from tasks module
                subject = "Welcome to Quack!"
                content_html = f"""
                    <p>Hello <strong>{user_name}</strong>, <span class="duck-icon">🦆</span></p>
                    <p>Welcome to Quack! We're excited to have you on board.</p>
                    <p>Thank you for joining our platform. If you have any questions, 
                    please don't hesitate to contact us.</p>
                """
                footer_html = "<p>The Quack Team <span class='duck-icon'>🦆</span></p>"

                html_body = render_template_string(
                    NEOBRUTALIST_HTML_TEMPLATE,
                    subject=subject,
                    title="Welcome to Quack!",
                    content=content_html,
                    footer=footer_html,
                )

                text_body = f"""
                Hello {user_name},
                
                Welcome to Quack! We're excited to have you on board.
                
                Thank you for joining our platform. If you have any questions, 
                please don't hesitate to contact us.
                
                The Quack Team
                """

                send_email(
                    subject=subject,
                    recipients=[email],
                    text_body=text_body,
                    html_body=html_body,
                )
                click.echo(f"✅ Welcome email sent synchronously to {email}")
            else:
                send_welcome_email_task.delay(email, user_name)

        elif template == "notification":
            user_name = template_data.get("name", "Test User")
            subject = template_data.get("subject", "Important Notification")
            message = template_data.get(
                "message", "This is a test notification message from Quack."
            )

            if sync:
                # Use the template from email module, not from tasks module
                content_html = f"""
                    <p>Hello <strong>{user_name}</strong>, <span class="duck-icon">🦆</span></p>
                    <p>{message}</p>
                """
                footer_html = "<p>The Quack Team <span class='duck-icon'>🦆</span></p>"

                html_body = render_template_string(
                    NEOBRUTALIST_HTML_TEMPLATE,
                    subject=subject,
                    title=subject,
                    content=content_html,
                    footer=footer_html,
                )

                text_body = f"""
                Hello {user_name},
                
                {message}
                
                The Quack Team
                """

                send_email(
                    subject=subject,
                    recipients=[email],
                    text_body=text_body,
                    html_body=html_body,
                )
                click.echo(f"✅ Notification email sent synchronously to {email}")
            else:
                send_notification_email_task.delay(subject, email, user_name, message)

        elif template == "account_status":
            user_name = template_data.get("name", "Test User")
            status = template_data.get("status", "approved")
            reason = template_data.get("reason", "Test reason")

            if sync:
                # Use the template from email module, not from tasks module
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
                        f"Reason: {reason}",
                        f"Reason: <span class='highlight'>{reason}</span>",
                    )

                subject = f"Account {status.capitalize()} - Quack"

                content_html = f"""
                    <p>Hello <strong>{user_name}</strong>, <span class="duck-icon">🦆</span></p>
                    <p>{html_message}</p>
                    <p>If you have any questions, please contact our support team.</p>
                """
                footer_html = "<p>The Quack Team <span class='duck-icon'>🦆</span></p>"

                html_body = render_template_string(
                    NEOBRUTALIST_HTML_TEMPLATE,
                    subject=subject,
                    title=f"Account {status.capitalize()}",
                    content=content_html,
                    footer=footer_html,
                )

                text_body = f"""
                Hello {user_name},
                
                {text_message}
                
                If you have any questions, please contact our support team.
                
                The Quack Team
                """

                send_email(
                    subject=subject,
                    recipients=[email],
                    text_body=text_body,
                    html_body=html_body,
                )
                click.echo(
                    f"✅ Account status ({status}) email sent synchronously to {email}"
                )
            else:
                send_account_status_email_task.delay(email, user_name, status, reason)

        elif template == "newsletter":
            subject = template_data.get("subject", "Quack Newsletter")
            campaign_name = template_data.get("campaign_name", "Test Campaign")
            content = template_data.get(
                "content",
                "<p>This is a test newsletter content. It could contain <strong>formatted text</strong>, images, and links.</p>",
            )
            
            if sync:
                # Use the template from email module directly
                content_html = f"""
                    <p><span class="duck-icon">🦆</span> Important announcement from Quack! <span class="duck-icon">🦆</span></p>
                    <div>{content}</div>
                    <hr>
                    <p><small>You're receiving this because you subscribed to our newsletter.
                """
                
                footer_html = "<p>The Quack Team <span class='duck-icon'>🦆</span></p>"
                
                html_body = render_template_string(
                    NEOBRUTALIST_HTML_TEMPLATE,
                    subject=subject,
                    title=campaign_name,
                    content=content_html,
                    footer=footer_html
                )
                
                text_body = f"""
                {campaign_name}
                
                {content.replace('<p>', '').replace('</p>', '\n').replace('<strong>', '').replace('</strong>', '')}
                
                ---
                You're receiving this because you subscribed to our newsletter.
                To unsubscribe, click here: [unsubscribe link]
                
                The Quack Team
                """
                
                send_email(
                    subject=subject,
                    recipients=[email],
                    text_body=text_body,
                    html_body=html_body,
                )
                click.echo(f"✅ Newsletter email sent synchronously to {email}")
            else:
                send_newsletter_email_task.delay([email], subject, campaign_name, content)

        elif template == "profile_update":
            user_name = template_data.get("name", "Test User")
            updated_fields = template_data.get(
                "updated_fields", ["name", "email", "address", "phone"]
            )
            
            if sync:
                # Create HTML list items for the fields
                fields_html = "".join([f"<li><strong>{field}</strong></li>" for field in updated_fields])
                fields_str = ", ".join(updated_fields)
                
                subject = "Profile Updated - Quack"
                
                content_html = f"""
                    <p>Hello <strong>{user_name}</strong>, <span class="duck-icon">🦆</span></p>
                    <p>Your profile has been successfully updated. The following information was changed:</p>
                    <ul>
                        {fields_html}
                    </ul>
                    <p>If you did not make these changes, please contact our support team immediately.</p>
                """
                
                footer_html = "<p>The Quack Team <span class='duck-icon'>🦆</span></p>"
                
                html_body = render_template_string(
                    NEOBRUTALIST_HTML_TEMPLATE,
                    subject=subject,
                    title="Profile Updated",
                    content=content_html,
                    footer=footer_html
                )
                
                text_body = f"""
                Hello {user_name},
                
                Your profile has been successfully updated. The following information was changed:
                {fields_str}
                
                If you did not make these changes, please contact our support team immediately.
                
                The Quack Team
                """
                
                send_email(
                    subject=subject,
                    recipients=[email],
                    text_body=text_body,
                    html_body=html_body,
                )
                click.echo(f"✅ Profile update email sent synchronously to {email}")
            else:
                send_profile_update_email_task.delay(email, user_name, updated_fields)

        elif template == "admin_notification":
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
            
            if sync:
                # Format details dict into HTML for HTML email
                details_html = "".join([f"<li><strong>{k}:</strong> {v}</li>" for k, v in details.items()])
                details_str = "\n".join([f"{k}: {v}" for k, v in details.items()])
                
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
                    subject=subject,
                    title=f"Admin Notification: {event_type}",
                    content=content_html,
                    footer=footer_html
                )
                
                text_body = f"""
                Admin Notification: {event_type}
                
                Event Details:
                {details_str}
                
                This is an automated message from the Quack system.
                """
                
                send_email(
                    subject=subject,
                    recipients=[email],
                    text_body=text_body,
                    html_body=html_body,
                )
                click.echo(f"✅ Admin notification email sent synchronously to {email}")
            else:
                send_admin_notification_email_task.delay(
                    email, subject, event_type, details
                )

        else:  # neobrutalist
            if sync:
                # Direct call to the email function without Celery
                from ..email import send_test_email

                result = send_test_email(email)
                if result["status"] == "success":
                    click.echo(
                        f"✅ Neobrutalist test email sent synchronously to {email}"
                    )
                else:
                    click.echo(f"❌ Error sending email: {result['message']}", err=True)
            else:
                send_test_email_task.delay(email)

        if not sync:
            click.echo(f"✅ {template.capitalize()} template email queued for {email}")
            if template_data:
                click.echo(f"📄 Template data: {json.dumps(template_data, indent=2)}")

    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)
        if not sync:
            click.echo(
                "Try using --sync flag to bypass Celery/Redis: flask test-email user@example.com --sync"
            )


@click.command("check-email-config")
@with_appcontext
def check_email_config_cmd():
    """Check if email configuration is properly set up."""
    result = check_email_config()

    click.echo("\nEmail Configuration Status:")
    click.echo(f"  MAIL_SERVER: {result['config']['MAIL_SERVER']}")
    click.echo(f"  MAIL_PORT: {result['config']['MAIL_PORT']}")
    click.echo(f"  MAIL_USE_TLS: {result['config']['MAIL_USE_TLS']}")
    click.echo(
        f"  MAIL_USERNAME: {'Set ✓' if result['config']['MAIL_USERNAME'] else 'Not set ✗'}"
    )
    click.echo(
        f"  MAIL_PASSWORD: {'Set ✓' if result['config']['MAIL_PASSWORD'] else 'Not set ✗'}"
    )
    click.echo(f"  MAIL_DEFAULT_SENDER: {result['config']['MAIL_DEFAULT_SENDER']}")
    click.echo(
        f"\nOverall configuration: {'✅ Complete' if result['is_configured'] else '❌ Incomplete'}"
    )

    if result["is_configured"]:
        click.echo("\nTest your email configuration with one of these commands:")
        click.echo("  flask test-email your-email@example.com")
        click.echo(
            "  flask test-email your-email@example.com --sync  # No Redis/Celery needed"
        )
        click.echo("\nOr see all available templates with:")
        click.echo("  flask list-email-templates")

    click.echo(
        "\nNOTE: If Redis is not running, use the --sync flag to send emails synchronously:"
    )
    click.echo("  flask test-email your-email@example.com --sync")

    # Check Redis connection
    try:
        import redis

        r = redis.Redis()
        r.ping()
        click.echo("\nRedis status: ✅ Connected")
    except:
        click.echo("\nRedis status: ❌ Not connected")
        click.echo("To start Redis: brew services start redis")
        click.echo(
            "Or use the --sync flag to bypass Redis: flask test-email your-email@example.com --sync"
        )


@click.command("list-email-templates")
@with_appcontext
def list_email_templates_cmd():
    """List all available email templates for testing."""
    templates = {
        "welcome": "Welcome email for new users",
        "notification": "General notification email",
        "account_status": "Account status change notification (approved, rejected, blocked, unblocked)",
        "newsletter": "Marketing/newsletter email",
        "profile_update": "Profile update confirmation",
        "admin_notification": "Admin alerts",
        "neobrutalist": "Full demonstration of neobrutalist design",
    }

    click.echo("\n🦆 Available Email Templates 🦆\n")

    for name, description in templates.items():
        click.echo(f"  • {name}")
        click.echo(f"    {description}")

        # Show sample command
        if name == "neobrutalist":
            click.echo(f"    Example: flask test-email user@example.com")
        elif name == "account_status":
            click.echo(
                f'    Example: flask test-email user@example.com -t {name} -d \'{{"status": "approved"}}\''
            )
        else:
            click.echo(f"    Example: flask test-email user@example.com -t {name}")
        click.echo("")

    click.echo("For more detailed usage:")
    click.echo("  flask test-email --help")

    # Add information about sync mode
    click.echo("\nSending emails without Redis/Celery:")
    click.echo(
        "  Add the --sync flag to send emails synchronously and bypass Redis/Celery"
    )
    click.echo("  Example: flask test-email user@example.com --sync")
    click.echo("  Example: flask test-email user@example.com -t welcome --sync")
