from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Модель пользователя, наследуемая от AbstractUser.

    Атрибуты:
        email (EmailField): Уникальный адрес электронной почты пользователя.
        phone (CharField): Телефон пользователя.
        tg_nick (CharField): Ник пользователя в Telegram.
        tg_chat_id (CharField): Chat ID пользователя в Telegram.
        city (CharField): Город пользователя.
    """
    username = None
    email = models.EmailField(unique=True, verbose_name="Почта", help_text="Введите Вашу почту.")
    phone = models.CharField(max_length=35, blank=True, null=True, verbose_name="Телефон",
                             help_text="Введите Ваш телефон.")
    tg_nick = models.CharField(max_length=50, blank=True, null=True, verbose_name="ТГ ник",
                               help_text="Введите Ваш ник в Telegram.")
    tg_chat_id = models.CharField(max_length=50, blank=True, null=True, verbose_name="ТГ chat-id",
                                  help_text="Введите Ваш chat-id в Telegram.")
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name="Город", help_text="Введите Ваш город.")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
