from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from exercise.models import Exercise


class ExerciseDetailViewTests(APITestCase):

    def setUp(self):
        self.exercise = Exercise.objects.create(name="Test Exercise", description="This is a test exercise.")

    def test_get_exercise_detail(self):
        url = reverse('exercise_detail', kwargs={'exercise_id': self.exercise.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.exercise.name)
        self.assertEqual(response.data['description'], self.exercise.description)


class ExerciseListViewTests(APITestCase):

    def setUp(self):
        Exercise.objects.create(name="Exercise 1", description="This is the first test exercise.")
        Exercise.objects.create(name="Exercise 2", description="This is the second test exercise.")

    def test_get_exercise_list(self):
        url = reverse('list_exercise')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], "Exercise 1")
        self.assertEqual(response.data[1]['name'], "Exercise 2")
