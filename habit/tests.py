from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from habit.models import WorkSession
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
