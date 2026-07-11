import csv
import os

from tasks.celery_app import celery
from models.models import Application

@celery.task
def export_student_applications(student_id):

    applications = Application.query.filter_by(student_id=student_id).all()

    os.makedirs("exports", exist_ok=True)

    filename = f"student_{student_id}_applications.csv"
    filepath = os.path.join("exports", filename)

    with open(filepath, "w", newline="") as csv_file:

        writer = csv.writer(csv_file)

        writer.writerow([
            "Application ID",
            "Job Title",
            "Company",
            "Status",
            "Interview Date"
        ])

        for application in applications:

            writer.writerow([
                application.id,
                application.job.title,
                application.job.company.company_name,
                application.status,
                application.interview_date
            ])

    return filepath