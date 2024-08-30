from rest_framework.permissions import BasePermission

from habit.models import Habit, HabitInstance, Reminder


class IsReminderCreator(BasePermission):
    message = "You do not have access to this reminder"

    def has_permission(self, request, view):
        user = request.user
        reminder = Reminder.objects.get(id=view.kwargs['reminder_id'])

        return user == reminder.user_creator


class IsRecurringHabitCreator(BasePermission):
    message = "You do not have access to this habit"

    def has_permission(self, request, view):
        user = request.user
        habit = Habit.objects.get(id=view.kwargs['habit_id'])

        return user == habit.user_creator

