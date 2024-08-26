from rest_framework import serializers

from scoring.models import UserScore, Feature, PurchasedFeature


class UserScoreOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserScore
        fields = ['id', 'score']


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = '__all__'


class PurchasedFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchasedFeature
        fields = '__all__'
