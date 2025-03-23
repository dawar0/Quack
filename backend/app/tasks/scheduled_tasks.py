# app/tasks/scheduled_tasks.py
from app.celery_utils import celery_app
from app import create_app  # Import create_app to get the application context
import time


@celery_app.task(bind=True)
def example_task(self):
    """A simple example task."""
    for i in range(5):
        print(f"Example task running: {i}")
        time.sleep(1)
    return "Example task finished!"


@celery_app.task(bind=True)
def daily_reminder_task(self):
    """Task to send daily reminders."""
    app = create_app()
    with app.app_context():
        # Logic to check for pending service requests and send reminders
        print("Sending daily reminders...")
        # Replace this with your actual implementation (using Google Chat, SMS, or email)
        return "Daily reminders sent."


@celery_app.task(bind=True)
def monthly_activity_report_task(self):
    """Task to generate and send monthly activity reports."""
    app = create_app()
    with app.app_context():
        # Logic to generate the monthly report and send it via email
        print("Generating and sending monthly activity report...")
        # Replace this with your actual implementation
        return "Monthly activity report sent."


@celery_app.task(bind=True)
def export_closed_requests_csv_task(self):
    """Task to export closed service requests to CSV."""
    app = create_app()
    with app.app_context():
        # Logic to fetch closed service requests and generate CSV
        print("Exporting closed service requests to CSV...")
        # Replace this with your actual implementation
        return "Closed service requests exported to CSV."
