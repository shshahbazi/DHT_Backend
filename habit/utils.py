from datetime import timedelta

from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.utils import timezone
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

    send_reminder_task.apply_async((habit_instance.id,), eta=reminder_time)

    return habit_instance
