from celery import shared_task
from django.utils import timezone
from datetime import timedelta, datetime
from habits.models import Habit
from habits.services import send_telegram_message
import random

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

    Напоминания отправляются за час и за 10 минут до выполнения привычки.
    """
    now = timezone.localtime()
    current_time = now.time()
    habits = Habit.objects.all()

    for habit in habits:
        habit_time = datetime.combine(now.date(), habit.time)
        notify_time_1 = (habit_time - timedelta(hours=1)).time()
        notify_time_2 = (habit_time - timedelta(minutes=10)).time()

        # Проверка времени для отправки уведомлений за час
        if notify_time_1 <= current_time <= (datetime.combine(now.date(), notify_time_1) + timedelta(minutes=1)).time():
            send_reminder(habit)

        # Проверка времени для отправки уведомлений за 10 минут
        if notify_time_2 <= current_time <= (datetime.combine(now.date(), notify_time_2) + timedelta(minutes=1)).time():
            send_reminder(habit)


def send_reminder(habit):
    """ Отправляет напоминание о привычке пользователю."""
    tg_chat = habit.owner.tg_chat_id
    name = habit.owner.tg_nick if habit.owner.tg_nick else 'Дорогой пользователь'
    if habit.is_pleasant:
        message = (f"Привет, {name}!\n\nНе забудьте насладиться Вашей приятной привычкой: "
                   f"{habit.action} в {habit.time.strftime('%H:%M')} в условленном месте ({habit.place}).\n\n")
    else:
        reward_message = ""
        if habit.related_habit:
            related_action = Habit.objects.get(id=habit.related_habit_id).action
            reward_message = f"После выполнения, можете насладиться: {related_action}.\n\n"
        elif habit.reward:
            reward_message = f"После выполнения, можете наградить себя: {habit.reward}.\n\n"

        message = (f"Привет, {name}!\n\nНе забудьте выполнить свою привычку: "
                   f"{habit.action} в {habit.time.strftime('%H:%M')} в условленном месте ({habit.place}).\n\n"
                   f"{reward_message}{get_random_message()}")

    send_telegram_message(tg_chat, message)
