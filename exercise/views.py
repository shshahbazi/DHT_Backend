from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from exercise.models import Exercise
from exercise.serializers import ExerciseSerializer


class ExerciseDetailView(APIView):
    @swagger_auto_schema(responses={200: ExerciseSerializer()})
    def get(self, request, exercise_id):
        exercise = Exercise.objects.get(id=exercise_id)
        serializer = ExerciseSerializer(exercise)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ExerciseListView(APIView):
    @swagger_auto_schema(responses={200: ExerciseSerializer(many=True)})
    def get(self, request):
        exercises = Exercise.objects.all()
        serializer = ExerciseSerializer(instance=exercises, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
