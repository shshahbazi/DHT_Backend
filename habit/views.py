from django.db.models import Q
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from common.permissions import IsRecurringHabitCreator, IsReminderCreator
from habit.models import WorkSession, Habit, HabitInstance, ToDoItem, Reminder
from habit.serializers import WorkSessionStartSerializer, ChangeHabitInstanceStatusSerializer, HabitInstanceSerializer, \
    RecurringHabitSerializer, ToDoItemSerializer, InputToDoItemSerializer, \
    UserHabitSuggestionSerializer, ReminderSerializer
from habit.utils import create_periodic_task_instance, delete_recurring_habit_instances, create_reminder_celery_task, \
    update_reminder_task, delete_reminder_task


class WorkSessionStartApi(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: None}, tags=['WorkSession'])
    def get(self, request):
        """
        a user must have one not ended work session
        if user have not ended work session it returns error and end session api should be called
        """
        user = request.user
        serializer = WorkSessionStartSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        work_session = WorkSession.objects.create(user=user, start_time=serializer.validated_data['start_time'])

        tasks = Habit.objects.filter((Q(user_creator=None) | Q(user_creator=user)) & (Q(is_active=True)))
        for task in tasks:
            create_periodic_task_instance(user=user, task=task)

        return Response(status=status.HTTP_200_OK)


class WorkSessionEndApi(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: None}, tags=['WorkSession'])
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

    @swagger_auto_schema(
        request_body=ChangeHabitInstanceStatusSerializer(),
        responses={200: HabitInstanceSerializer()},
        tags=['HabitInstance']
    )
    def put(self, request, habit_instance_id):
        habit_instance = HabitInstance.objects.get(id=habit_instance_id)
        serializer = ChangeHabitInstanceStatusSerializer(instance=habit_instance, data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        output_serializer = HabitInstanceSerializer(instance=habit_instance)

        return Response(output_serializer.data, status=status.HTTP_200_OK)


class CreateReminderApi(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=ReminderSerializer, responses={201: ReminderSerializer()}, tags=['Reminder']
    )
    def post(self, request):
        serializer = ReminderSerializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)

        new_reminder = serializer.save()
        create_reminder_celery_task(new_reminder)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CreateRecurringHabitApi(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=RecurringHabitSerializer, responses={201: RecurringHabitSerializer()}, tags=['RecurringHabit']
    )
    def post(self, request):
        serializer = RecurringHabitSerializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)

        new_habit = serializer.save()
        # I don't know if this should be done or not:
        # create_periodic_task_instance(request.user, new_habit)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RecurringHabitDetailApi(APIView):
    permission_classes = [IsAuthenticated, IsRecurringHabitCreator]

    @swagger_auto_schema(responses={200: RecurringHabitSerializer()}, tags=['RecurringHabit'])
    def get(self, request, habit_id):
        habit = Habit.objects.get(id=habit_id)
        serializer = RecurringHabitSerializer(instance=habit)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={200: None}, tags=['RecurringHabit'])
    def delete(self, request, habit_id):
        habit = Habit.objects.get(id=habit_id)
        delete_recurring_habit_instances(habit)
        habit.delete()
        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=RecurringHabitSerializer, responses={200: RecurringHabitSerializer()}, tags=['RecurringHabit']
    )
    def put(self, request, habit_id):
        # TODO: should pending instances change?
        habit = Habit.objects.get(id=habit_id)
        serializer = RecurringHabitSerializer(instance=habit, data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReminderDetailApi(APIView):
    permission_classes = [IsAuthenticated, IsReminderCreator]

    @swagger_auto_schema(responses={200: ReminderSerializer()}, tags=['Reminder'])
    def get(self, request, reminder_id):
        reminder = Reminder.objects.get(id=reminder_id)
        serializer = ReminderSerializer(instance=reminder)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={200: None}, tags=['Reminder'])
    def delete(self, request, reminder_id):
        reminder = Reminder.objects.get(id=reminder_id)
        delete_reminder_task(reminder)
        reminder.delete()
        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=ReminderSerializer, responses={200: ReminderSerializer()}, tags=['Reminder']
    )
    def put(self, request, reminder_id):
        reminder = Reminder.objects.get(id=reminder_id)

        serializer = ReminderSerializer(instance=reminder, data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)

        new_reminder = serializer.save()
        update_reminder_task(new_reminder)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserHabitsListApi(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: RecurringHabitSerializer(many=True)}, tags=['RecurringHabits'])
    def get(self, request):
        user = request.user

        recurring_habits = Habit.objects.filter(user_creator__in=[user, None])

        serializer = RecurringHabitSerializer(recurring_habits, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserReminderListApi(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: ReminderSerializer(many=True)}, tags=['Reminder'])
    def get(self, request):
        user = request.user
        reminders = Reminder.objects.filter(user_creator=user)
        serializer = ReminderSerializer(reminders, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class AddToDoItemApi(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=InputToDoItemSerializer(), responses={201: ToDoItemSerializer()}, tags=['ToDoList'])
    def post(self, request):
        user = request.user
        serializer = InputToDoItemSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ToDoItemDetailApi(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: ToDoItemSerializer()}, tags=['ToDoList'])
    def get(self, request, pk):
        item = ToDoItem.objects.get(pk=pk)
        serializer = ToDoItemSerializer(item, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=ToDoItemSerializer(), responses={200: ToDoItemSerializer()}, tags=['ToDoList'])
    def put(self, request, pk):
        item = ToDoItem.objects.get(pk=pk)
        serializer = ToDoItemSerializer(instance=item, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={200: None}, tags=['ToDoList'])
    def delete(self, request, pk):
        item = ToDoItem.objects.get(pk=pk)
        item.delete()
        return Response(status=status.HTTP_200_OK)


class GetToDoListApi(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: ToDoItemSerializer(many=True)}, tags=['ToDoList'])
    def get(self, request):
        user = request.user
        todo_items = user.todolist.items.all()

        sorted_items = sorted(
            todo_items,
            key=lambda item: (item.done, item.deadline)
        )
        serializer = ToDoItemSerializer(sorted_items, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class SubmitUserHabitSuggestionApi(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=UserHabitSuggestionSerializer(), responses={201: UserHabitSuggestionSerializer()}, tags=['Suggestion']
    )
    def post(self, request):
        user = request.user
        serializer = UserHabitSuggestionSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
