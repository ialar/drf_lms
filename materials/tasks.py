from celery import shared_task
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER
from materials.models import Course
from users.models import Subscription


@shared_task
def send_email_about_update(course_id):
    """Отправляет письма подписчикам при обновлении курса."""
    print("Отправка писем подписчикам ...")
    course = Course.objects.get(pk=course_id)
    updates = Subscription.objects.filter(course=course_id)
    for update in updates:
        send_mail(
            subject="Обновление курса!",
            message=f"Ваш курс {course.name} был обновлен. Пожалуйста, проверьте изменения.",
            from_email=EMAIL_HOST_USER,
            recipient_list=[f"{update.user.email}"],
            fail_silently=True
        )
