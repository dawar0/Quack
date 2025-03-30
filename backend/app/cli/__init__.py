from .email_commands import register_email_commands
from .cache_commands import register_cache_commands


def register_cli_commands(app):
    """Register all CLI commands with the application."""
    register_email_commands(app)
    register_cache_commands(app)
