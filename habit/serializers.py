from django.utils import timezone
from rest_framework import serializers, exceptions

from habit.models import WorkSession


class WorkSessionStartSerializer(serializers.Serializer):
    start_time = serializers.SerializerMethodField(required=False)

    def validate(self, attrs):
        user = self.context['request'].user

        work_sessions = WorkSession.objects.filter(user=user, end_time=None).exists()
        if work_sessions:
            raise exceptions.ValidationError("You should end your last work session")

        attrs['start_time'] = timezone.now()

        return attrs


# class WorkSessionEndSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = WorkSession
#         fields = ['end_time']


class WorkSessionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkSession
        fields = '__all__'


