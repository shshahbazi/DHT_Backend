from django.db.models import Q
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from habit.models import WorkSession, RecurringHabit, HabitInstance, SingleHabit
from habit.serializers import WorkSessionStartSerializer, ChangeHabitInstanceStatusSerializer, HabitInstanceSerializer, \
    SingleHabitSerializer, RecurringHabitSerializer
from habit.utils import create_periodic_task_instance, create_single_task_instance


class WorkSessionStartApi(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: None})
    def get(self, request):
        """
        a user must have one not ended work session
        if user have not ended work session it returns error and end session api should be called
        """
        user = request.user
        serializer = WorkSessionStartSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        work_session = WorkSession.objects.create(user=user, start_time=serializer.validated_data['start_time'])

        tasks = RecurringHabit.objects.filter(Q(user_creator=None) | Q(user_creator=user))
        for task in tasks:
            create_periodic_task_instance(user=user, task=task)

        return Response(status=status.HTTP_200_OK)


class WorkSessionEndApi(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: None})
    def get(self, request):
        end_time = timezone.now()
        user = request.user

        work_session = WorkSession.objects.filter(user=user, end_time=None).first()
        if work_session:
            work_session.end_time = end_time
            work_session.save()

        return Response(status=status.HTTP_200_OK)


class EndHabitInstanceApi(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=ChangeHabitInstanceStatusSerializer(), responses={200: HabitInstanceSerializer()})
    def put(self, request, habit_instance_id):
        habit_instance = HabitInstance.objects.get(id=habit_instance_id)
        serializer = ChangeHabitInstanceStatusSerializer(instance=habit_instance, data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        output_serializer = HabitInstanceSerializer(instance=habit_instance)

        return Response(output_serializer.data, status=status.HTTP_200_OK)


class CreateSingleHabitApi(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=SingleHabitSerializer, responses={201: SingleHabitSerializer()})
    def post(self, request):
        serializer = SingleHabitSerializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)

        new_habit = serializer.save()
        create_single_task_instance(request.user, new_habit)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CreateRecurringHabitApi(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=RecurringHabitSerializer, responses={201: RecurringHabitSerializer()})
    def post(self, request):
        serializer = RecurringHabitSerializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)

        new_habit = serializer.save()
        # I don't know if this should be done or not:
        # create_periodic_task_instance(request.user, new_habit)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RecurringHabitDetailApi(APIView):

    @swagger_auto_schema(responses={200: RecurringHabitSerializer()})
    def get(self, request, habit_id):
        habit = RecurringHabit.objects.get(id=habit_id)
        serializer = RecurringHabitSerializer(instance=habit)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={200: None})
    def delete(self, request, habit_id):
        habit = RecurringHabit.objects.get(id=habit_id)
        habit.delete()
        return Response(status=status.HTTP_200_OK)


class SingleHabitDetailApi(APIView):

    @swagger_auto_schema(responses={200: SingleHabitSerializer()})
    def get(self, request, habit_id):
        habit = SingleHabit.objects.get(id=habit_id)
        serializer = SingleHabitSerializer(instance=habit)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={200: None})
    def delete(self, request, habit_id):
        # TODO: Check what should be happened to instances of that habit
        habit = SingleHabit.objects.get(id=habit_id)
        habit.delete()
        return Response(status=status.HTTP_200_OK)

