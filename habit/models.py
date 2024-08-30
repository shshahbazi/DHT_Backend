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
    score = models.PositiveIntegerField(default=1)
    recurrence_seconds = models.IntegerField()
    duration_seconds = models.IntegerField(default=0)

    # class Meta:
    #     abstract = True


# class SingleHabit(Habit):
#     reminder_time = models.DateTimeField()
#     instances = GenericRelation('HabitInstance', related_query_name='single_habits')


# class RecurringHabit(Habit):
#     recurrence_seconds = models.IntegerField()
#     duration_seconds = models.IntegerField(default=0)
#     instances = GenericRelation('HabitInstance', related_query_name='recurring_habits')


class HabitInstance(BaseModel):
    class STATUS(models.TextChoices):
        DONE = "DONE", "Done"
        PENDING = "PENDING", "Pending"
        UNDONE = "UNDONE", "Undone"
        NOTIFIED = "NOTIFIED", "Notified"

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name="instances")
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


class ToDoList(BaseModel):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)


class ToDoItem(BaseModel):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    done = models.BooleanField(default=False)
    deadline = models.DateTimeField(blank=True, null=True)
    list = models.ForeignKey(ToDoList, on_delete=models.CASCADE, related_name='items')


class UserHabitSuggestion(BaseModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='suggestions')
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    score = models.PositiveIntegerField(default=1)


class Reminder(BaseModel):
    user_creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reminders')
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    reminder_time = models.DateTimeField()
    celery_task_id = models.CharField(max_length=200, blank=True, null=True)
