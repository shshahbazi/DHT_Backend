from rest_framework import serializers

from scoring.models import UserScore, Feature


class UserScoreOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserScore
        fields = ['id', 'score']


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = '__all__'
