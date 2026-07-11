from tasks.celery_app import celery

@celery.task
def test_task():
    return "Celery Working Successfully"