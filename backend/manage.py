import os
from app import create_app
from app.database import db
from app import models
from flask_migrate import Migrate, upgrade, migrate, init, downgrade
import click
from seed_data import seed_database

app = create_app()
migrate = Migrate(app, db)


@app.cli.command("seed")
@click.option("--drop", is_flag=True, help="Drop all tables before seeding.")
def seed_db(drop):
    """Seeds the database with initial data."""
    if drop:
        with app.app_context():
            db.drop_all()
            db.create_all()
            print("Tables dropped and recreated.")

    print("Seeding database...")
    seed_database()


if __name__ == "__main__":
    # No need for manager.run() with Flask CLI
    pass
