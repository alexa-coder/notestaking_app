# users/tests.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User

class UserTests(APITestCase):
    def test_user_registration(self):
        url = reverse('register')
        data = {'user_name': 'Test User', 'user_email': 'test@example.com', 'password': 'testpass123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().user_email, 'test@example.com')

    def test_duplicate_registration(self):
        url = reverse('register')
        data = {'user_name': 'Test User', 'user_email': 'test@example.com', 'password': 'testpass123'}
        self.client.post(url, data, format='json')
        # Attempt to register same email again
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_token_auth(self):
        # Create a user directly
        User.objects.create_user(user_email='test@example.com', user_name='Test User', password='testpass123')
        # Obtain JWT token
        response = self.client.post(reverse('token_obtain_pair'),
                                    {'user_email': 'test@example.com', 'password': 'testpass123'},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)