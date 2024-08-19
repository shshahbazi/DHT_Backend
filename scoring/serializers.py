from rest_framework import serializers

from scoring.models import UserScore


class UserScoreOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserScore
        fields = ['id', 'score']
