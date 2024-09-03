from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from habit.models import WorkSession, Habit
from user.models import CustomUser


class WorkSessionTests(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(email='test@example.com', password='password123')
        self.client.force_authenticate(user=self.user)

    def test_start_work_session(self):
        response = self.client.get(reverse('start_work'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(WorkSession.objects.filter(user=self.user, end_time=None).exists())

    def test_end_work_session(self):
        work_session = WorkSession.objects.create(user=self.user, start_time=timezone.now())
        response = self.client.get(reverse('end_work'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        work_session.refresh_from_db()
        self.assertIsNotNone(work_session.end_time)


class HabitTests(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(email='test@example.com', password='password123')
        self.client.force_authenticate(user=self.user)

    def test_edit_habit(self):
        habit = Habit.objects.create(user_creator=self.user, name="Test Habit", recurrence_seconds=86400)
        data = {
            "name": "عادت ویرایش شده",
            "recurrence_seconds": 72000,
            "duration_seconds": 3600
        }
        response = self.client.put(reverse('recurring_habit', kwargs={'habit_id': habit.id}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        habit.refresh_from_db()
        self.assertEqual(habit.name, "عادت ویرایش شده")

    def test_delete_habit(self):
        habit = Habit.objects.create(user_creator=self.user, name="عادت تست", recurrence_seconds=86400)
        response = self.client.delete(reverse('recurring_habit', kwargs={'habit_id': habit.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Habit.objects.filter(id=habit.id).exists())
