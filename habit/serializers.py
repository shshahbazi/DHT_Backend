from django.utils import timezone
from rest_framework import serializers, exceptions

from habit.models import WorkSession, HabitInstance, SingleHabit, RecurringHabit
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

        if isinstance(instance.habit, RecurringHabit):
            create_periodic_task_instance(instance.user, instance.habit)

        return instance


class SingleHabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = SingleHabit
        fields = '__all__'


class RecurringHabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecurringHabit
        fields = '__all__'


class HabitInstanceSerializer(serializers.ModelSerializer):
    habit_detail = serializers.SerializerMethodField()
    content_type_name = serializers.CharField(source='content_type.model')

    class Meta:
        model = HabitInstance
        exclude = ['object_id', 'content_type']

    def get_habit_detail(self, obj):
        model_class = obj.content_type.model_class()
        if model_class == SingleHabit:
            return SingleHabitSerializer(obj.habit).data
        elif model_class == RecurringHabit:
            return RecurringHabitSerializer(obj.habit).data
        return None