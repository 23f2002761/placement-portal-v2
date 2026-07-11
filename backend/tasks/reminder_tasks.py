from datetime import datetime, timedelta
from flask_mail import Message

from tasks.celery_app import celery
from extensions import mail
from models.models import Application


@celery.task
def send_interview_reminders():

    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

    interviews = Application.query.filter(
        Application.interview_date == tomorrow
    ).all()

    for application in interviews:

        msg = Message(
            subject="Interview Reminder",
            recipients=["ash769980@gmail.com"]
        )

        msg.body = f"""
Hello {application.student.name},

This is a reminder for your interview.

Company: {application.job.company.company_name}
Job Title: {application.job.title}

Interview Date: {application.interview_date}
Interview Mode: {application.interview_mode}
Interview Location: {application.interview_location}

Best of luck!

Placement Portal
"""

        mail.send(msg)

    return f"Sent {len(interviews)} reminder(s)"