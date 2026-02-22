from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Habit

User = get_user_model()


class HabitTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.habit_data = {
            "place": "Дом",
            "time": "10:00:00",
            "action": "Сделать зарядку",
            "duration": 60,
            "periodicity": 1,
            "is_pleasant": False,
            "is_public": False,
        }

    def test_create_habit(self):
        """Тест создания привычки"""
        response = self.client.post("/habits/", self.habit_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 1)
        self.assertEqual(Habit.objects.first().action, "Сделать зарядку")

    def test_create_habit_with_reward(self):
        """Тест создания привычки с вознаграждением"""
        data = self.habit_data.copy()
        data["reward"] = "Чашка кофе"
        response = self.client.post("/habits/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.first().reward, "Чашка кофе")

    def test_create_habit_without_auth(self):
        """Тест создания без авторизации"""
        anonymous_client = APIClient()
        response = anonymous_client.post("/habits/", self.habit_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_habits(self):
        """Тест списка привычек"""
        Habit.objects.create(user=self.user, **self.habit_data)
        response = self.client.get("/habits/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        self.assertEqual(len(response.data["results"]), 1)

    def test_public_habits(self):
        """Тест публичных привычек"""
        public_data = self.habit_data.copy()
        public_data["is_public"] = True
        Habit.objects.create(user=self.user, **public_data)

        anonymous_client = APIClient()
        response = anonymous_client.get("/habits/public/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        self.assertEqual(len(response.data["results"]), 1)

    def test_habit_detail(self):
        """Тест просмотра конкретной привычки"""
        habit = Habit.objects.create(user=self.user, **self.habit_data)
        response = self.client.get(f"/habits/{habit.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["action"], "Сделать зарядку")

    def test_update_habit(self):
        """Тест обновления привычки"""
        habit = Habit.objects.create(user=self.user, **self.habit_data)
        response = self.client.patch(f"/habits/{habit.id}/", {"action": "Обновленное действие"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        habit.refresh_from_db()
        self.assertEqual(habit.action, "Обновленное действие")

    def test_delete_habit(self):
        """Тест удаления привычки"""
        habit = Habit.objects.create(user=self.user, **self.habit_data)
        response = self.client.delete(f"/habits/{habit.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.count(), 0)

    def test_habit_validation_duration_too_long(self):
        """Тест валидации: время выполнения > 120 секунд"""
        data = self.habit_data.copy()
        data["duration"] = 121
        response = self.client.post("/habits/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_habit_validation_reward_and_linked(self):
        """Тест валидации: нельзя reward и linked_habit одновременно"""
        pleasant_data = self.habit_data.copy()
        pleasant_data["action"] = "Послушать музыку"
        pleasant_data["is_pleasant"] = True
        pleasant_habit = Habit.objects.create(user=self.user, **pleasant_data)

        data = self.habit_data.copy()
        data["reward"] = "Кофе"
        data["linked_habit"] = pleasant_habit.id
        response = self.client.post("/habits/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_habit_validation_linked_not_pleasant(self):
        """Тест валидации: связанная привычка должна быть приятной"""
        not_pleasant_data = self.habit_data.copy()
        not_pleasant_data["action"] = "Полезное дело"
        not_pleasant_habit = Habit.objects.create(user=self.user, **not_pleasant_data)

        data = self.habit_data.copy()
        data["linked_habit"] = not_pleasant_habit.id
        response = self.client.post("/habits/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_habit_validation_pleasant_with_reward(self):
        data = self.habit_data.copy()
        data["is_pleasant"] = True
        data["reward"] = "Кофе"
        response = self.client.post("/habits/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_habit_validation_periodicity_too_high(self):
        data = self.habit_data.copy()
        data["periodicity"] = 8
        response = self.client.post("/habits/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
