import click
from flask.cli import with_appcontext
from ..utils.cache_management import clear_cache, list_cache_keys, get_cache_stats


def register_cache_commands(app):
    """Register cache-related CLI commands with the application."""
    app.cli.add_command(purge_cache_cmd)
    app.cli.add_command(list_cache_cmd)
    app.cli.add_command(cache_stats_cmd)


@click.command("purge-cache")
@click.option(
    "--pattern",
    "-p",
    default="*",
    help="Pattern of keys to purge (e.g. 'user:*' for all user keys)",
)
@click.option(
    "--confirm",
    "-y",
    is_flag=True,
    default=False,
    help="Skip confirmation prompt",
)
@with_appcontext
def purge_cache_cmd(pattern, confirm):
    """
    Purge Redis cache keys matching the specified pattern.

    Examples:

    \b
    # Purge all cache keys (with confirmation)
    flask purge-cache

    \b
    # Purge all user-related cache keys
    flask purge-cache -p "user:*"

    \b
    # Purge all cache keys without confirmation
    flask purge-cache -y
    """
    if pattern != "*":
        keys = list_cache_keys(pattern)
        if not keys:
            click.echo(f"No keys found matching pattern: {pattern}")
            return

        click.echo(f"Found {len(keys)} keys matching pattern: {pattern}")
        if len(keys) <= 10:
            click.echo("Keys to be purged:")
            for key in keys:
                click.echo(f"  - {key}")
    else:
        count = len(list_cache_keys("*"))
        click.echo(f"This will purge ALL {count} keys in the Redis cache!")

    if not confirm:
        if not click.confirm("Do you want to continue?"):
            click.echo("Operation cancelled.")
            return

    purged = clear_cache(pattern)
    click.echo(f"✅ Successfully purged {purged} keys from Redis cache.")


@click.command("list-cache")
@click.option(
    "--pattern",
    "-p",
    default="*",
    help="Pattern of keys to list",
)
@click.option(
    "--limit",
    "-l",
    default=50,
    help="Maximum number of keys to display",
)
@with_appcontext
def list_cache_cmd(pattern, limit):
    """
    List Redis cache keys matching the specified pattern.

    Examples:

    \b
    # List all cache keys (limited to 50)
    flask list-cache

    \b
    # List user-related cache keys
    flask list-cache -p "user:*"

    \b
    # List all keys with a higher limit
    flask list-cache -l 100
    """
    keys = list_cache_keys(pattern)

    if not keys:
        click.echo(f"No keys found matching pattern: {pattern}")
        return

    total = len(keys)
    displayed = min(total, limit)

    click.echo(f"Found {total} keys matching pattern: {pattern}")
    click.echo(f"Displaying {displayed} keys:")

    for i, key in enumerate(keys[:limit]):
        click.echo(f"  {i+1}. {key}")

    if total > limit:
        click.echo(f"... and {total - limit} more keys not shown")


@click.command("cache-stats")
@with_appcontext
def cache_stats_cmd():
    """
    Display Redis cache statistics.

    Example:

    \b
    flask cache-stats
    """
    try:
        stats = get_cache_stats()

        click.echo("\n📊 Redis Cache Statistics 📊\n")
        click.echo(f"  Total keys: {stats['total_keys']}")
        click.echo(f"  Memory used: {stats['used_memory_human']}")
        click.echo(f"  Connected clients: {stats['connected_clients']}")
        click.echo(f"  Uptime: {stats['uptime_in_days']} days")

        click.echo("\nTo purge the cache:")
        click.echo("  flask purge-cache")
        click.echo("\nTo list cache keys:")
        click.echo("  flask list-cache")
    except Exception as e:
        click.echo(f"❌ Error connecting to Redis: {str(e)}", err=True)
        click.echo("Make sure Redis server is running.")
