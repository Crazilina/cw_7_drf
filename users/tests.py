from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from datetime import datetime, timezone


class UserTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email="testuser@example.com",
            phone="1234567890",
            tg_nick="test_tg_nick",
            tg_chat_id="123456789",
            city="Test City"
        )
        self.client.force_authenticate(user=self.user)
        self.other_user = User.objects.create(
            email="otheruser@example.com",
            phone="0987654321",
            tg_nick="other_tg_nick",
            tg_chat_id="987654321",
            city="Other City"
        )

    def test_user_retrieve(self):
        url = reverse('users:user-detail', args=[self.user.id])
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('email'), self.user.email)
        self.assertEqual(data.get('phone'), self.user.phone)
        self.assertEqual(data.get('tg_nick'), self.user.tg_nick)
        self.assertEqual(data.get('tg_chat_id'), self.user.tg_chat_id)
        self.assertEqual(data.get('city'), self.user.city)

    def test_user_create(self):
        url = reverse('users:user-list')
        data = {
            "email": "newuser@example.com",
            "password": "newpassword",
            "phone": "1234567890",
            "tg_nick": "newtgnick",
            "tg_chat_id": "newtgchatid",
            "city": "New City"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.all().count(), 3)

    def test_user_update(self):
        url = reverse('users:user-detail', args=[self.user.id])
        data = {
            "email": "updateduser@example.com",
            "phone": "0987654321",
            "tg_nick": "updatedtgnick",
            "tg_chat_id": "updatedtgchatid",
            "city": "Updated City"
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data.get('email'), "updateduser@example.com")
        self.assertEqual(data.get('phone'), "0987654321")
        self.assertEqual(data.get('tg_nick'), "updatedtgnick")
        self.assertEqual(data.get('tg_chat_id'), "updatedtgchatid")
        self.assertEqual(data.get('city'), "Updated City")

    def test_user_delete(self):
        url = reverse('users:user-detail', args=[self.user.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.all().count(), 1)

    @staticmethod
    def normalize_date(date_str):
        dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return dt.astimezone(timezone.utc).isoformat().replace('+00:00', 'Z')

    def test_user_list(self):
        url = reverse('users:user-list')
        response = self.client.get(url)
        data = response.json()

        for user_data in data:
            user_data["date_joined"] = self.normalize_date(user_data["date_joined"])

        result = [
            {
                "id": self.user.id,
                "last_login": self.user.last_login.isoformat().replace('+00:00', 'Z') if self.user.last_login else None,
                "is_superuser": self.user.is_superuser,
                "first_name": self.user.first_name,
                "last_name": self.user.last_name,
                "is_staff": self.user.is_staff,
                "is_active": self.user.is_active,
                "date_joined": self.user.date_joined.isoformat().replace('+00:00', 'Z'),
                "email": self.user.email,
                "phone": self.user.phone,
                "tg_nick": self.user.tg_nick,
                "tg_chat_id": self.user.tg_chat_id,
                "city": self.user.city,
                "groups": [],
                "user_permissions": []
            },
            {
                "id": self.other_user.id,
                "last_login": self.other_user.last_login.isoformat().replace('+00:00',
                                                                             'Z') if self.other_user.last_login
                else None,
                "is_superuser": self.other_user.is_superuser,
                "first_name": self.other_user.first_name,
                "last_name": self.other_user.last_name,
                "is_staff": self.other_user.is_staff,
                "is_active": self.other_user.is_active,
                "date_joined": self.other_user.date_joined.isoformat().replace('+00:00', 'Z'),
                "email": self.other_user.email,
                "phone": self.other_user.phone,
                "tg_nick": self.other_user.tg_nick,
                "tg_chat_id": self.other_user.tg_chat_id,
                "city": self.other_user.city,
                "groups": [],
                "user_permissions": []
            }
        ]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)
