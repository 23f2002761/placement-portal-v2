from datetime import datetime
from flask_mail import Message

from tasks.celery_app import celery
from extensions import mail
from models.models import (
    Student,
    Company,
    JobPosition,
    Application,
    Placement
)

@celery.task
def generate_monthly_report():

    total_students = Student.query.count()
    total_companies = Company.query.count()
    total_jobs = JobPosition.query.count()
    total_applications = Application.query.count()
    total_placements = Placement.query.count()

    html = f"""
    <h2>Monthly Placement Report</h2>

    <table border="1" cellpadding="8">
        <tr>
            <th>Metric</th>
            <th>Count</th>
        </tr>

        <tr>
            <td>Total Students</td>
            <td>{total_students}</td>
        </tr>

        <tr>
            <td>Total Companies</td>
            <td>{total_companies}</td>
        </tr>

        <tr>
            <td>Total Jobs</td>
            <td>{total_jobs}</td>
        </tr>

        <tr>
            <td>Total Applications</td>
            <td>{total_applications}</td>
        </tr>

        <tr>
            <td>Total Placements</td>
            <td>{total_placements}</td>
        </tr>
    </table>
    """

    msg = Message(
        subject="Monthly Placement Report",
        recipients=["ash769980@gmail.com"]     
    )

    msg.html = html

    mail.send(msg)

    return "Monthly report sent successfully."