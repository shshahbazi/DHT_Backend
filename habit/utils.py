from datetime import timedelta

from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.utils import timezone

from habit.models import RecurringHabit, HabitInstance


def create_periodic_task_instance(user, task):
    reminder_time = timezone.now() + timedelta(seconds=task.recurrence_seconds + task.duration_seconds)

    habit_instance = HabitInstance.objects.create(
        user=user,
        content_type=ContentType.objects.get_for_model(RecurringHabit),
        object_id=task.id,
        reminder_time=reminder_time
    )
    return habit_instance
