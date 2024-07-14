from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from habits.models import Habit
from django.test import TestCase
from rest_framework.serializers import ValidationError
from habits.validators import validate_habit


class HabitTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="testuser@example.com")
        self.client.force_authenticate(user=self.user)
        self.habit = Habit.objects.create(
            owner=self.user,
            action="Test Habit",
            time="12:00:00",
            place="Home",
            is_pleasant=True,
            period=1,
            reward="Reward",
            execution_time=60,
            is_public=True
        )

    def test_habit_retrieve(self):
        url = reverse('habits:habit-retrieve', args=[self.habit.id])
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('action'), self.habit.action)
        self.assertEqual(data.get('time'), self.habit.time)
        self.assertEqual(data.get('place'), self.habit.place)
        self.assertEqual(data.get('is_pleasant'), self.habit.is_pleasant)
        self.assertEqual(data.get('period'), self.habit.period)
        self.assertEqual(data.get('reward'), self.habit.reward)
        self.assertEqual(data.get('execution_time'), self.habit.execution_time)
        self.assertEqual(data.get('is_public'), self.habit.is_public)

    def test_habit_create(self):
        url = reverse('habits:habit-create')
        data = {
            "action": "New Habit",
            "time": "14:00:00",
            "place": "Office",
            "is_pleasant": False,
            "period": 1,
            "reward": "",
            "execution_time": 30,
            "is_public": False
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.all().count(), 2)

    def test_habit_update(self):
        url = reverse('habits:habit-update', args=[self.habit.id])
        data = {
            "action": "Updated Habit",
            "time": "15:00:00",
            "place": "Office",
            "is_pleasant": False,
            "period": 7,
            "reward": "New Reward",
            "execution_time": 90,
            "is_public": False
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data.get("action"), "Updated Habit")
        self.assertEqual(data.get('time'), "15:00:00")
        self.assertEqual(data.get('place'), "Office")
        self.assertEqual(data.get('is_pleasant'), False)
        self.assertEqual(data.get('period'), 7)
        self.assertEqual(data.get('reward'), "New Reward")
        self.assertEqual(data.get('execution_time'), 90)
        self.assertEqual(data.get('is_public'), False)

    def test_habit_delete(self):
        url = reverse('habits:habit-delete', args=[self.habit.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.all().count(), 0)

    def test_habit_list(self):
        url = reverse('habits:habit-list')
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.habit.id,
                    "owner": self.habit.owner.id,
                    "action": self.habit.action,
                    "time": self.habit.time,
                    "place": self.habit.place,
                    "is_pleasant": self.habit.is_pleasant,
                    "related_habit": self.habit.related_habit,
                    "period": self.habit.period,
                    "reward": self.habit.reward,
                    "execution_time": self.habit.execution_time,
                    "is_public": self.habit.is_public,
                }
            ]
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)


class HabitValidatorTests(TestCase):

    def setUp(self):
        self.valid_data = {
            "reward": None,
            "related_habit": None,
            "execution_time": 60,
            "is_pleasant": False,
            "period": 7
        }

    def test_valid_habit(self):
        try:
            validate_habit(self.valid_data)
        except ValidationError:
            self.fail("validate_habit() raised ValidationError unexpectedly!")

    def test_invalid_execution_time(self):
        data = self.valid_data.copy()
        data["execution_time"] = 130
        with self.assertRaises(ValidationError):
            validate_habit(data)

    def test_invalid_reward_and_related_habit(self):
        data = self.valid_data.copy()
        data["reward"] = "Reward"
        data["related_habit"] = "Related Habit"
        with self.assertRaises(ValidationError):
            validate_habit(data)

    def test_invalid_period(self):
        data = self.valid_data.copy()
        data["period"] = 10
        with self.assertRaises(ValidationError):
            validate_habit(data)
