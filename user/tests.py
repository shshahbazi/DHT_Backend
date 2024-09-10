from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from user.models import CustomUser, Profile


class UserAuthTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email='test@example.com', password='password123')

    def test_logout_user(self):
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        url = reverse('logout')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Token.objects.filter(user=self.user).exists())


class ProfileTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email='test@example.com', password='password123')
        self.profile = Profile.objects.get(user=self.user)
        self.profile.first_name = 'Test'
        self.profile.last_name = 'User'
        self.profile.save()
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_get_profile_details(self):
        url = reverse('profile-detail')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'Test')
        self.assertEqual(response.data['last_name'], 'User')

    def test_update_profile(self):
        url = reverse('profile-detail')
        data = {'first_name': 'Updated', 'last_name': 'User'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.first_name, 'Updated')

    def test_update_profile_picture_not_allowed(self):
        self.profile.allowed_change_profile = False
        self.profile.save()

        url = reverse('profile-picture')
        image = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        response = self.client.put(url, {'picture': image}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_profile_picture_allowed(self):
        self.profile.allowed_change_profile = True
        self.profile.save()

        url = reverse('profile-picture')
        image = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        response = self.client.put(url, {'picture': image}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
