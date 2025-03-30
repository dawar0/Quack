from flask import current_app, render_template_string
from .utils.email import send_email
import os
import time


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


def send_test_email(recipient_email):
    """
    Send a test email to verify email functionality

    Args:
        recipient_email: Email address to send the test email to

    Returns:
        dict: Dictionary containing the status of the email send attempt
    """
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    subject = f"Quack Test Email - {timestamp}"

    text_body = f"""
    This is a test email from the Quack application with neobrutalist design.
    
    If you're receiving this, email functionality is working correctly.
    
    Time sent: {timestamp}
    
    -- 
    Quack Team 🦆
    """

    content_html = f"""
        <div style="border-left: 10px solid #ff6b6b; padding-left: 15px; margin-bottom: 25px; transform: rotate(-1deg);">
            <p style="font-size: 20px; font-weight: bold;">Hello there, <span class="duck-icon">🦆</span></p>
            <p>This is a <strong>test email</strong> from Quack to verify that email functionality is working correctly.</p>
            <p class="highlight" style="transform: rotate(1deg); display: inline-block; padding: 10px; font-weight: bold; font-size: 18px;">
                If you received this email, your email configuration is set up correctly! <span class="duck-icon">🦆</span>
            </p>
        </div>
        
        <h2 style="margin-top:30px; transform: rotate(-1deg); background-color: #fff45c; display: inline-block; padding: 10px 15px; border: 3px solid #000; box-shadow: 5px 5px 0 #000;">Time Sent: {timestamp}</h2>
        
    """

    footer_html = """
    <p style="font-size: 18px; font-weight: bold;">The Quack Team <span class='duck-icon'>🦆</span></p>
    <div style="background-color: #a2ffe9; padding: 8px; border: 1px solid #000; display: inline-block; transform: rotate(-1deg); margin-top: 10px;">
        <p style="margin: 0; font-size: 12px;">This is a system generated test email. Please do not reply.</p>
    </div>
    """

    try:
        html_body = render_template_string(
            NEOBRUTALIST_HTML_TEMPLATE,
            subject=subject,
            title="EMAIL TEST SUCCESSFUL!",
            content=content_html,
            footer=footer_html,
        )

        send_email(
            subject=subject,
            recipients=[recipient_email],
            text_body=text_body,
            html_body=html_body,
        )

        return {"status": "success", "message": f"Test email sent to {recipient_email}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def check_email_config():
    """
    Check if email configuration is properly set up

    Returns:
        dict: Dictionary containing configuration status
    """
    config = {
        "MAIL_SERVER": current_app.config.get("MAIL_SERVER"),
        "MAIL_PORT": current_app.config.get("MAIL_PORT"),
        "MAIL_USE_TLS": current_app.config.get("MAIL_USE_TLS"),
        "MAIL_USERNAME": bool(current_app.config.get("MAIL_USERNAME")),
        "MAIL_PASSWORD": bool(current_app.config.get("MAIL_PASSWORD")),
        "MAIL_DEFAULT_SENDER": current_app.config.get("MAIL_DEFAULT_SENDER"),
    }

    is_configured = all(
        [
            config["MAIL_SERVER"],
            config["MAIL_PORT"],
            config["MAIL_USERNAME"],
            config["MAIL_PASSWORD"],
            config["MAIL_DEFAULT_SENDER"],
        ]
    )

    return {"config": config, "is_configured": is_configured}
