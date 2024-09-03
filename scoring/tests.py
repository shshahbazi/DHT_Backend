from django.test import TestCase
from rest_framework.test import APITestCase

from scoring.models import UserScore
from user.models import CustomUser


class UserScoreTests(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(email='test@example.com', password='password123')
        self.user_score = UserScore.objects.get(user=self.user)
        self.user_score.score = 100
        self.user_score.save()
        self.client.force_authenticate(user=self.user)

    def test_add_points(self):
        self.user_score.add_points(50)
        self.assertEqual(self.user_score.score, 150)

    def test_sub_points(self):
        self.user_score.sub_points(50)
        self.assertEqual(self.user_score.score, 50)

    def test_sub_points_below_zero(self):
        self.user_score.sub_points(150)
        self.assertEqual(self.user_score.score, 0)
