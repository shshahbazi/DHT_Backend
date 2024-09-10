from django.utils import timezone
from rest_framework import serializers, exceptions

from mental.models import DailyMood


class MoodTrackerSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyMood
        fields = ['mood']

    def create(self, validated_data):
        user = self.context['request'].user

        daily_mood = DailyMood.objects.filter(created_at__day=timezone.now().day, user=user).first()

        if daily_mood:
            daily_mood.mood = validated_data['mood']

        else:
            daily_mood = DailyMood.objects.create(**validated_data, user=user)

        return daily_mood