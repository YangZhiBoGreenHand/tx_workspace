from app.celery.celery_app import celery_app


@celery_app.task
def add(x, y):
    print("Adding two numbers")
    return x + y
