from celery import shared_task
from django.utils import timezone
from habits.models import Habit
from .services import send_telegram_message
import random
import logging

logger = logging.getLogger(__name__)


MOTIVATIONAL_MESSAGES = [
    "Продолжайте в том же духе и достигайте своих целей!",
    "Вы на правильном пути! Продолжайте в том же духе!",
    "Ваши усилия приносят плоды! Так держать!",
    "Каждый шаг приближает Вас к успеху!",
    "Вы можете всё! Главное не останавливаться!",
    "Ваше упорство - ключ к успеху!",
    "Вы сильнее, чем думаете!",
    "Не сдавайтесь, Вы уже так далеко зашли!",
    "Действуйте сегодня ради лучшего завтра!",
    "Каждое Ваше действие приближает Вас к цели!",
    "Ваши привычки формируют Ваше будущее!",
    "Маленькие шаги ведут к большим достижениям!",
    "Ваши усилия не пройдут даром!",
    "Продолжайте, Вы делаете отличную работу!",
    "Ваш успех неизбежен, если Вы не остановитесь!",
    "Верьте в себя и свои силы!",
    "Каждый день - новая возможность для успеха!",
    "Сделайте сегодня ещё один шаг к своей мечте!",
    "Ваше стремление и упорство вдохновляют!",
    "Продолжайте работать над собой, и Вы увидите результаты!"
]


def get_random_message():
    return random.choice(MOTIVATIONAL_MESSAGES)


@shared_task
def send_habit_reminders():
    """
    Отправляет напоминания пользователям о выполнении привычек.
    """
    now = timezone.localtime(timezone.now())
    current_time = now.time()
    habits = Habit.objects.filter(time__hour=current_time.hour, time__minute=current_time.minute)

    for habit in habits:
        tg_chat = habit.owner.tg_chat_id
        if habit.is_pleasant:
            message = (f"Привет, {habit.owner.email}!\n\nНе забудьте насладиться Вашей приятной привычкой: "
                       f"{habit.action} в {habit.time.strftime('%H:%M')} в {habit.place}.\n\n")
        else:
            message = (f"Привет, {habit.owner.email}!\n\nНе забудьте выполнить свою привычку: "
                       f"{habit.action} в {habit.time.strftime('%H:%M')} в {habit.place}.\n\n"
                       f"{get_random_message()}")
        send_telegram_message(tg_chat, message)

