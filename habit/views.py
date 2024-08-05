from django.db.models import Q
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from habit.models import WorkSession, RecurringHabit
from habit.serializers import WorkSessionStartSerializer
from habit.utils import create_periodic_task_instance


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

        print(serializer.validated_data)

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

        work_session = WorkSession.objects.filter(user=user).first()
        if work_session:
            work_session.end_time = end_time
            work_session.save()

        return Response(status=status.HTTP_200_OK)

