from datetime import timedelta

from celery.result import AsyncResult
from django.db import transaction
from django.utils import timezone
from django.core import exceptions
from rest_framework import exceptions

from .tasks import send_habit_task, send_reminder_task

from habit.models import Habit, HabitInstance


def create_periodic_task_instance(user, task):
    reminder_time = timezone.now() + timedelta(seconds=task.recurrence_seconds + task.duration_seconds)

    habit_instance = HabitInstance.objects.create(
        user=user,
        habit=task,
        reminder_time=reminder_time
    )

    celery_task = send_habit_task.apply_async((habit_instance.id,), eta=reminder_time)
    habit_instance.celery_task_id = celery_task.id
    habit_instance.save()

    return habit_instance


def create_reminder_celery_task(reminder):
    reminder_time = reminder.reminder_time

    celery_task = send_reminder_task.apply_async((reminder.id,), eta=reminder_time)

    reminder.celery_task_id = celery_task.id
    reminder.save()


def update_reminder_task(reminder):
    with transaction.atomic():
        try:
            if reminder.celery_task_id:
                task_result = AsyncResult(reminder.celery_task_id)
                task_result.revoke(terminate=True)

        except Exception as e:
            raise exceptions.APIException(f"Failed to revoke previous task: {str(e)}")

        try:
            celery_task = send_reminder_task.apply_async((reminder.id,), eta=reminder.reminder_time)
            reminder.celery_task_id = celery_task.id
            reminder.save()

        except Exception as e:
            raise exceptions.APIException(f"Failed to schedule new task: {str(e)}")

    return reminder


def delete_reminder_task(reminder):
    with transaction.atomic():
        try:
            if reminder.celery_task_id:
                task_result = AsyncResult(reminder.celery_task_id)
                task_result.revoke(terminate=True)

        except Exception as e:
            raise exceptions.APIException(f"Failed to revoke previous task: {str(e)}")


def delete_recurring_habit_instances(habit):
    habit_instances = habit.instances.all().filter(status=HabitInstance.STATUS.PENDING)

    with transaction.atomic():
        try:
            for habit_instance in habit_instances:
                if habit_instance.celery_task_id:
                    task_result = AsyncResult(habit_instance.celery_task_id)
                    task_result.revoke(terminate=True)

        except Exception as e:
            raise exceptions.BadRequest(f"Failed to revoke previous task: {str(e)}")

    habit_instances.delete()

