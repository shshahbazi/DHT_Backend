from rest_framework.permissions import BasePermission

from habit.models import Habit, HabitInstance, SingleHabit, RecurringHabit


class IsSingleHabitCreator(BasePermission):
    message = "You do not have access to this habit"

    def has_permission(self, request, view):
        user = request.user
        habit = SingleHabit.objects.get(id=view.kwargs['habit_id'])

        return user == habit.user_creator


class IsRecurringHabitCreator(BasePermission):
    message = "You do not have access to this habit"

    def has_permission(self, request, view):
        user = request.user
        habit = RecurringHabit.objects.get(id=view.kwargs['habit_id'])

        return user == habit.user_creator

