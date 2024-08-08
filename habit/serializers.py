from django.utils import timezone
from rest_framework import serializers, exceptions

from habit.models import WorkSession, HabitInstance


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


class HabitInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HabitInstance
        fields = '__all__'
