from django.utils import timezone
from rest_framework import serializers, exceptions

from habit.models import WorkSession, HabitInstance, Habit, ToDoItem, ToDoList, \
    UserHabitSuggestion, Reminder, PushNotificationToken
from habit.utils import create_periodic_task_instance


class WorkSessionStartSerializer(serializers.Serializer):
    start_time = serializers.SerializerMethodField(required=False)

    def validate(self, attrs):
        user = self.context['request'].user

        work_sessions = WorkSession.objects.filter(user=user, end_time=None).exists()
        if work_sessions:
            raise exceptions.ValidationError("You should end your last work session")

        attrs['start_time'] = timezone.now()

        return attrs


class WorkSessionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkSession
        fields = '__all__'


class ChangeHabitInstanceStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = HabitInstance
        fields = ['status']

    def save(self, **kwargs):
        instance = self.instance

        if 'status' in self.validated_data:
            instance.ended_at = timezone.now()

        instance = super().save(**kwargs)

        create_periodic_task_instance(instance.user, instance.habit)

        return instance


class ReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reminder
        read_only_fields = ['user_creator']
        exclude = ['celery_task_id']

    def save(self, **kwargs):
        user_creator = self.context['user']

        self.validated_data['user_creator'] = user_creator
        instance = super().save(**kwargs)

        return instance


class RecurringHabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'
        read_only_fields = ['user_creator']

    def validate(self, attrs):
        user_creator = self.context['user']
        if user_creator.profile.allowed_habits_count < 1:
            raise exceptions.ValidationError("You are not allowed to create new habit")
        return attrs

    def save(self, **kwargs):
        user_creator = self.context['user']

        self.validated_data['user_creator'] = user_creator
        instance = super().save(**kwargs)
        user_creator.profile.allowed_habits_count -= 1
        user_creator.profile.save()

        return instance


class HabitInstanceSerializer(serializers.ModelSerializer):
    habit = RecurringHabitSerializer()

    class Meta:
        model = HabitInstance
        fields = '__all__'


class InputToDoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToDoItem
        fields = ['title', 'description', 'deadline', 'list']
        read_only_fields = ['list']

    def validate(self, attrs):
        user = self.context['request'].user
        todo_list = ToDoList.objects.filter(user=user).first()

        attrs['list'] = todo_list
        return attrs


class ToDoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToDoItem
        exclude = ['list', 'created_at', 'updated_at']


class UserHabitSuggestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserHabitSuggestion
        fields = '__all__'
        read_only_fields = ['user']

    def validate(self, attrs):
        user = self.context['request'].user
        attrs['user'] = user
        return attrs


class PushNotificationTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = PushNotificationToken
        fields = '__all__'
