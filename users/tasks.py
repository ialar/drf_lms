from celery import shared_task
from django.utils import timezone

from users.models import User


@shared_task
def checks_user_activity():
    """Блокирует пользователей, которые не заходили более месяца."""
    users = User.objects.filter(is_active=True)
    for user in users:
        last_login_date = user.last_login
        now = timezone.now()
        month = timezone.timedelta(days=30)
        month_absence_date = now - month
        if last_login_date and month_absence_date >= last_login_date:
            user.is_active = False
            user.save()
            print(f"{user.email} заблокирован")
