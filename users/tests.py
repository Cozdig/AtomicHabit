from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


class UserTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {"username": "testuser", "email": "test@example.com", "password": "testpass123"}

    def test_register_user(self):
        """Тест регистрации пользователя"""
        response = self.client.post("/users/register/", self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertEqual(User.objects.count(), 1)

    def test_register_user_invalid_data(self):
        """Тест регистрации с невалидными данными"""
        response = self.client.post("/users/register/", {"username": "", "password": "123"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_user(self):
        """Тест авторизации пользователя"""
        User.objects.create_user(username="testuser", password="testpass123")

        response = self.client.post("/users/login/", {"username": "testuser", "password": "testpass123"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_invalid_credentials(self):
        """Тест авторизации с неверными данными"""
        response = self.client.post("/users/login/", {"username": "wrong", "password": "wrong"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_token_refresh(self):
        """Тест обновления токена"""
        register_response = self.client.post("/users/register/", self.user_data)
        refresh_token = register_response.data["refresh"]

        response = self.client.post("/users/token/refresh/", {"refresh": refresh_token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
