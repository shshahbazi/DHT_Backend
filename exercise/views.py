from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from exercise.models import Exercise
from exercise.serializers import ExerciseSerializer
import mental.utils as utils


class ExerciseDetailView(APIView):
    @swagger_auto_schema(responses={200: ExerciseSerializer()}, tags=['Exercise'])
    def get(self, request, exercise_id):
        exercise = Exercise.objects.get(id=exercise_id)
        serializer = ExerciseSerializer(exercise, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)


class ExerciseListView(APIView):
    @swagger_auto_schema(responses={200: ExerciseSerializer(many=True)}, tags=['Exercise'])
    def get(self, request):
        exercises = Exercise.objects.all()
        serializer = ExerciseSerializer(instance=exercises, many=True, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)
