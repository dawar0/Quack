from .email_commands import register_email_commands


def register_cli_commands(app):
    """Register all CLI commands with the application."""
    register_email_commands(app)
