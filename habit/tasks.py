from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from rest_framework import exceptions

from .models import HabitInstance, WorkSession, Reminder
from django.core.mail import EmailMessage
from datetime import timedelta


@shared_task
def send_habit_task(habit_instance_id):
    try:
        habit_instance: HabitInstance = HabitInstance.objects.get(id=habit_instance_id)
        if habit_instance.is_completed():
            return

        if WorkSession.objects.filter(user=habit_instance.user, end_time=None).exists():
            send_habit_notification(habit_instance)
            habit_instance.status = HabitInstance.STATUS.NOTIFIED
            habit_instance.save()

    except HabitInstance.DoesNotExist:
        pass


@shared_task
def send_reminder_task(reminder_id):
    try:
        reminder_instance: Reminder = Reminder.objects.get(id=reminder_id)

        if WorkSession.objects.filter(user=reminder_instance.user_creator, end_time=None).exists():
            send_reminder_notification(reminder_instance)

    except Reminder.DoesNotExist:
        pass


def send_reminder_notification(reminder_instance):
    # TODO: sending web push notification instead of email!
    try:
        email_body = f'سلام دوست عزیز \nالان زمان رسیدگی به یادآوری {reminder_instance.id} است\n{reminder_instance.id}\n'
        email = EmailMessage(subject='یادآوری عادت', body=email_body, to=[reminder_instance.user_creator.email])
        email.send()
    except Exception as e:
        raise exceptions.APIException(f'An error occurred while sending notification: {e}')


def send_habit_notification(habit_instance):
    # TODO: sending web push notification instead of email!
    try:
        email_body = f'سلام دوست عزیز \nالان زمان رسیدگی به عادت {habit_instance.id} است\n{habit_instance.id}\n {habit_instance.reminder_time}'
        email = EmailMessage(subject='یادآوری عادت', body=email_body, to=[habit_instance.user.email])
        email.send()
    except Exception as e:
        raise exceptions.APIException(f'An error occurred while sending notification: {e}')
