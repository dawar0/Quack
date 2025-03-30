# app/tasks/scheduled_tasks.py
from app.celery_utils import celery_app
from app import create_app
from app.models import User, ServiceRequest, Service
from sqlalchemy import and_, or_
from datetime import datetime, timedelta
from .email_tasks import send_email_task, send_notification_email_task
import time
import csv
import io
import os


@celery_app.task(bind=True)
def example_task(self):
    """A simple example task."""
    for i in range(5):
        print(f"Example task running: {i}")
        time.sleep(1)
    return "Example task finished!"


@celery_app.task(bind=True)
def daily_reminder_task(self):
    """Task to send daily reminders for pending service requests."""
    app = create_app()
    with app.app_context():
        # Get all pending service requests
        pending_requests = ServiceRequest.query.filter_by(
            service_status="pending"
        ).all()

        # Send reminder emails to customers with pending requests
        for request in pending_requests:
            if request.customer and request.customer.email:
                service_name = request.service.name if request.service else "service"

                # Send reminder to customer
                send_notification_email_task.delay(
                    subject="Reminder: Pending Service Request",
                    user_email=request.customer.email,
                    user_name=request.customer.name or request.customer.username,
                    message=f"This is a reminder that your request for {service_name} (Request #{request.id}) is still pending. "
                    f"We'll notify you when a professional accepts your request.",
                )

        # Send reminders to professionals about available service requests
        # Get all professionals who are approved
        professionals = (
            User.query.join(User.roles)
            .filter(
                and_(
                    User.status == "approved",
                    User.blocked == False,
                    User.profile_docs_verified == True,
                )
            )
            .all()
        )

        for professional in professionals:
            if professional.email:
                # Get count of pending requests that match professional's service type
                pending_count = (
                    ServiceRequest.query.join(Service)
                    .filter(
                        and_(
                            ServiceRequest.service_status == "pending",
                            ServiceRequest.professional_id == None,
                            (
                                Service.name.like(f"%{professional.service_type}%")
                                if professional.service_type
                                else True
                            ),
                        )
                    )
                    .count()
                )

                if pending_count > 0:
                    send_notification_email_task.delay(
                        subject="Available Service Requests",
                        user_email=professional.email,
                        user_name=professional.name or professional.username,
                        message=f"There are {pending_count} pending service requests available that match your expertise. "
                        f"Log in to view and accept these requests.",
                    )

        return "Daily reminders sent."


@celery_app.task(bind=True)
def monthly_activity_report_task(self):
    """Task to generate and send monthly activity reports to administrators."""
    app = create_app()
    with app.app_context():
        # Get admin users to send the report to
        admin_users = (
            User.query.join(User.roles)
            .filter(and_(Role.name == "admin", User.blocked == False))
            .all()
        )

        # Get monthly statistics
        now = datetime.utcnow()
        month_start = datetime(now.year, now.month, 1)

        # Count various metrics for the month
        new_users = User.query.filter(User.date_created >= month_start).count()
        new_requests = ServiceRequest.query.filter(
            ServiceRequest.date_of_request >= month_start
        ).count()
        completed_requests = ServiceRequest.query.filter(
            and_(
                ServiceRequest.service_status == "completed",
                ServiceRequest.date_of_completion >= month_start,
            )
        ).count()

        # Generate the report text
        report_text = f"""
Monthly Activity Report - {month_start.strftime('%B %Y')}

Summary:
- New users registered: {new_users}
- New service requests: {new_requests}
- Completed service requests: {completed_requests}
- Completion rate: {(completed_requests / new_requests * 100) if new_requests > 0 else 0:.2f}%

This report was automatically generated on {now.strftime('%Y-%m-%d %H:%M:%S')}.
        """

        # Generate HTML version
        report_html = f"""
<h1>Monthly Activity Report - {month_start.strftime('%B %Y')}</h1>

<h2>Summary:</h2>
<ul>
  <li>New users registered: <strong>{new_users}</strong></li>
  <li>New service requests: <strong>{new_requests}</strong></li>
  <li>Completed service requests: <strong>{completed_requests}</strong></li>
  <li>Completion rate: <strong>{(completed_requests / new_requests * 100) if new_requests > 0 else 0:.2f}%</strong></li>
</ul>

<p><em>This report was automatically generated on {now.strftime('%Y-%m-%d %H:%M:%S')}.</em></p>
        """

        # Send to all admins
        for admin in admin_users:
            if admin.email:
                send_email_task.delay(
                    subject=f"Monthly Activity Report - {month_start.strftime('%B %Y')}",
                    recipients=[admin.email],
                    text_body=report_text,
                    html_body=report_html,
                )

        return "Monthly activity report sent."


@celery_app.task(bind=True)
def export_closed_requests_csv_task(self):
    """Task to export closed service requests to CSV and email to administrators."""
    app = create_app()

    with app.app_context():
        # Get admin users to send the export to
        admin_users = (
            User.query.join(User.roles)
            .filter(and_(Role.name == "admin", User.blocked == False))
            .all()
        )

        # Get completed service requests from the last 30 days
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        completed_requests = ServiceRequest.query.filter(
            and_(
                ServiceRequest.service_status == "completed",
                ServiceRequest.date_of_completion >= thirty_days_ago,
            )
        ).all()

        # Create CSV in memory
        output = io.StringIO()
        writer = csv.writer(output)

        # Write header
        writer.writerow(
            [
                "Request ID",
                "Service",
                "Customer",
                "Customer Email",
                "Professional",
                "Professional Email",
                "Request Date",
                "Completion Date",
                "Status",
                "Location",
                "Remarks",
            ]
        )

        # Write data
        for request in completed_requests:
            writer.writerow(
                [
                    request.id,
                    request.service.name if request.service else "Unknown Service",
                    request.customer.name if request.customer else "Unknown Customer",
                    request.customer.email if request.customer else "",
                    request.professional.name if request.professional else "Unassigned",
                    request.professional.email if request.professional else "",
                    (
                        request.date_of_request.strftime("%Y-%m-%d")
                        if request.date_of_request
                        else ""
                    ),
                    (
                        request.date_of_completion.strftime("%Y-%m-%d")
                        if request.date_of_completion
                        else ""
                    ),
                    request.service_status,
                    request.location_pin_code,
                    request.remarks,
                ]
            )

        # Get the CSV data
        csv_data = output.getvalue()
        output.close()

        # Prepare the export date for the filename
        export_date = datetime.utcnow().strftime("%Y-%m-%d")

        # Send email with CSV attachment to admins
        for admin in admin_users:
            if admin.email:
                send_email_task.delay(
                    subject=f"Completed Service Requests Export - {export_date}",
                    recipients=[admin.email],
                    text_body=f"Attached is the CSV export of completed service requests for the last 30 days.",
                    html_body=f"<p>Attached is the CSV export of completed service requests for the last 30 days.</p>",
                    attachments=[
                        (f"completed_requests_{export_date}.csv", "text/csv", csv_data)
                    ],
                )

        return "Closed service requests exported to CSV and emailed."
