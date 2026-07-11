from celery import Celery
from app import app

def make_celery(app):
    celery = Celery(
        app.import_name,
        broker="redis://localhost:6379/0",
        backend="redis://localhost:6379/0"
    )

    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask

    return celery


celery = make_celery(app)

import tasks.test_tasks
import tasks.reminder_tasks
import tasks.report_tasks
import tasks.export_tasks