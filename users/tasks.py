from celery import shared_task


@shared_task
def checks_user_activity():
    ...
