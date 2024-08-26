from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from mental.models import DailyMood
from mental.serializers import MoodTrackerSerializer


class SubmitMood(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=MoodTrackerSerializer(), responses={200: None}, tags=['MoodTracker'])
    def post(self, request):
        serializer = MoodTrackerSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        daily_mood = serializer.create(validated_data=serializer.validated_data)
        daily_mood.save()

        return Response(status=status.HTTP_201_CREATED)
