from django.db import models
from users.models import User

NULLABLE = {'blank': True, 'null': True}

class Habit(models.Model):
    """
    Модель привычки.

    Атрибуты:
        owner (ForeignKey): Ссылка на пользователя, которому принадлежит привычка.
        action (CharField): Описание действия привычки.
        time (TimeField): Время выполнения привычки.
        place (CharField): Место выполнения привычки.
        is_pleasant (BooleanField): Флаг, указывающий, является ли привычка приятной.
        related_habit (ForeignKey): Ссылка на связанную привычку.
        period (PositiveIntegerField): Периодичность выполнения привычки в днях.
        reward (CharField): Вознаграждение за выполнение привычки.
        execution_time (PositiveIntegerField): Время на выполнение привычки в секундах.
        is_public (BooleanField): Флаг, указывающий, является ли привычка публичной.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habits', verbose_name="Владелец",
                             help_text="Укажите владельца.")
    action = models.CharField(max_length=255, verbose_name="Действие", help_text="Введите действие.")
    time = models.TimeField(verbose_name="Время", help_text="Введите время.")
    place = models.CharField(max_length=255, verbose_name="Место", help_text="Введите место.")
    is_pleasant = models.BooleanField(default=False, verbose_name="Приятная привычка", help_text="Приятная привычка?")
    related_habit = models.ForeignKey('self', **NULLABLE, on_delete=models.SET_NULL,
                                      related_name='related_to', verbose_name="Связанная привычка",
                                      help_text="Укажите связанную привычку.")
    period = models.PositiveIntegerField(default=1, verbose_name="Периодичность", help_text="Введите периодичность.")
    reward = models.CharField(max_length=255, **NULLABLE, verbose_name="Вознаграждение",
                              help_text="Введите вознаграждение.")
    execution_time = models.PositiveIntegerField(verbose_name="Время на выполнение",
                                                 help_text="Введите время в секундах.")
    is_public = models.BooleanField(default=False, verbose_name="Публичная привычка", help_text="Публичная привычка?")

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"

    def __str__(self):
        return f"{self.owner.email} - {self.action}"
