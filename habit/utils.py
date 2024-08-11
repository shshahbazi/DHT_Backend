from datetime import timedelta

from celery.result import AsyncResult
from celery.worker.control import revoke
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from django.core import exceptions

from .tasks import send_reminder_task

from habit.models import RecurringHabit, HabitInstance, SingleHabit


def create_periodic_task_instance(user, task):
    if not isinstance(task, RecurringHabit):
        return

    reminder_time = timezone.now() + timedelta(seconds=task.recurrence_seconds + task.duration_seconds)

    habit_instance = HabitInstance.objects.create(
        user=user,
        content_type=ContentType.objects.get_for_model(RecurringHabit),
        object_id=task.id,
        reminder_time=reminder_time
    )

    send_reminder_task.apply_async((habit_instance.id,), eta=reminder_time)
    return habit_instance


def create_single_task_instance(user, task):
    if not isinstance(task, SingleHabit):
        return

    reminder_time = task.reminder_time

    habit_instance = HabitInstance.objects.create(
        user=user,
        content_type=ContentType.objects.get_for_model(SingleHabit),
        object_id=task.id,
        reminder_time=reminder_time
    )

    celery_task = send_reminder_task.apply_async((habit_instance.id,), eta=reminder_time)

    habit_instance.celery_task_id = celery_task.id
    habit_instance.save()

    return habit_instance


def update_single_habit_instance_reminder(habit):
    if not isinstance(habit, SingleHabit):
        return

    habit_instance = habit.instances.all().first()

    with transaction.atomic():
        try:
            if habit_instance.celery_task_id:
                task_result = AsyncResult(habit_instance.celery_task_id)
                task_result.revoke(terminate=True)

        except Exception as e:
            raise exceptions.BadRequest(f"Failed to revoke previous task: {str(e)}")

        try:
            habit_instance.reminder_time = habit.reminder_time
            habit_instance.save()
        except Exception as e:
            raise exceptions.BadRequest(f"Failed to update habit instance: {str(e)}")

        try:
            celery_task = send_reminder_task.apply_async((habit_instance.id,), eta=habit.reminder_time)
            habit_instance.celery_task_id = celery_task.id
            habit_instance.save()

        except Exception as e:
            raise exceptions.BadRequest(f"Failed to schedule new task: {str(e)}")

    return habit_instance


def delete_single_habit_instance(habit):
    if not isinstance(habit, SingleHabit):
        return

    habit_instance = habit.instances.all().first()

    with transaction.atomic():
        try:
            if habit_instance.celery_task_id:
                task_result = AsyncResult(habit_instance.celery_task_id)
                task_result.revoke(terminate=True)

        except Exception as e:
            raise exceptions.BadRequest(f"Failed to revoke previous task: {str(e)}")

        habit_instance.delete()

