# __init__.py
import time
import asyncio
from flask import Flask
from sqlalchemy.exc import OperationalError
from .services.fetchingAPI.tasks import (
        fetch_and_save_teams,
        fetch_and_save_services,
        fetch_and_save_incidents,
        fetch_and_save_escalation_policies,
    )
from .extensions import db

# Constants
MAX_DB_RETRIES = 10
RETRY_WAIT_SECONDS = 5

def create_app():
    """Initialize and configure the Flask app."""
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Initialize the database
    db.init_app(app)

    # Retry logic for database connection
    with app.app_context():
        if not initialize_database():
            raise Exception("Failed to connect to the database after retries.")

        # Fetch and save initial data
        initialize_data()

    # Register blueprints
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

def initialize_database():
    """Attempt to initialize the database with retries."""
    retries = MAX_DB_RETRIES
    while retries > 0:
        try:
            from .models import Service, Incident, Team, EscalationPolicy  # Explicit import ensures models are registered
            db.create_all()
            print("Database initialized successfully.")
            return True
        except OperationalError:
            retries -= 1
            print(f"Database not ready. Retrying ({retries} retries left)...")
            time.sleep(RETRY_WAIT_SECONDS)
    return False


def initialize_data():
    """Fetch and save initial data into the database."""
    asyncio.run(async_initialize_data())

async def async_initialize_data():
    """Asynchronous helper to fetch and save initial data."""
    try:
        await asyncio.gather(
            fetch_and_save_teams(),
            fetch_and_save_services(),
            fetch_and_save_escalation_policies(),
        )
        # Fetch and save incidents after services
        await fetch_and_save_incidents()
        print("Initial data fetching completed successfully.")
    except Exception as e:
        print(f"Error during initial data fetching: {e}")
