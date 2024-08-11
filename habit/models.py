from celery.result import AsyncResult
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core import exceptions
from django.db import models, transaction

from common.models import BaseModel
from user.models import CustomUser


class Habit(BaseModel):
    user_creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class SingleHabit(Habit):
    reminder_time = models.DateTimeField()
    instances = GenericRelation('HabitInstance', related_query_name='single_habits')


class RecurringHabit(Habit):
    recurrence_seconds = models.IntegerField()
    duration_seconds = models.IntegerField(default=0)
    instances = GenericRelation('HabitInstance', related_query_name='recurring_habits')


class HabitInstance(BaseModel):
    class STATUS(models.TextChoices):
        DONE = "DONE", "Done"
        PENDING = "PENDING", "Pending"
        UNDONE = "UNDONE", "Undone"

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    habit = GenericForeignKey('content_type', 'object_id')
    # habit_type = models.CharField(max_length=200)
    status = models.CharField(max_length=200, choices=STATUS.choices, default=STATUS.PENDING)
    reminder_time = models.DateTimeField()
    ended_at = models.DateTimeField(blank=True, null=True)
    celery_task_id = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f'{self.user} - {self.habit} in {self.reminder_time}'

    def is_completed(self):
        return self.status == self.STATUS.DONE


class WorkSession(BaseModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)

