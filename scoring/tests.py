from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from scoring.models import UserScore, Feature, PurchasedFeature
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


class FeatureTests(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(email='test@example.com', password='password123')
        self.user_score = UserScore.objects.get(user=self.user)
        self.user_score.score = 100
        self.user_score.save()
        self.feature = Feature.objects.create(name="Test Feature", type="habit_limit", cost=50, habit_increase_amount=5)
        self.client.force_authenticate(user=self.user)

    def test_list_features(self):
        response = self.client.get(reverse('features-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_feature_detail(self):
        response = self.client.get(reverse('feature-detail', kwargs={'pk': self.feature.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Test Feature")


class PurchaseFeatureTests(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(email='test2@example.com', password='password123')
        self.feature = Feature.objects.create(name="Test Feature", type="habit_limit", cost=5, habit_increase_amount=5)
        self.client.force_authenticate(user=self.user)
        self.user_score = UserScore.objects.get(user=self.user)
        self.user_score.score = 100
        self.user_score.save()

    def test_purchase_feature_insufficient_score(self):
        self.user_score.score = 30
        self.user_score.save()
        response = self.client.get(reverse('purchase-feature', kwargs={'pk': self.feature.id}))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(PurchasedFeature.objects.filter(user=self.user, feature=self.feature).exists())
