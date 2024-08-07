from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from django.core import exceptions

from .models import HabitInstance
from django.core.mail import EmailMessage
from datetime import timedelta


@shared_task
def send_reminder_task(habit_instance_id):
    try:
        habit_instance: HabitInstance = HabitInstance.objects.get(id=habit_instance_id)
        if habit_instance.is_completed():
            return

        send_habit_notification(habit_instance)

    except HabitInstance.DoesNotExist:
        pass


def send_habit_notification(habit_instance):
    # TODO: sending web push notification instead of email!
    try:
        email_body = f'سلام دوست عزیز \nالان زمان رسیدگی به عادت {habit_instance.id} است\n{habit_instance.id}\n {habit_instance.reminder_time}'
        email = EmailMessage(subject='یادآوری عادت', body=email_body, to=[habit_instance.user.email])
        email.send()
    except Exception as e:
        raise exceptions.BadRequest(f'An error occurred while sending notification: {e}')
