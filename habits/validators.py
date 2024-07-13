from rest_framework.serializers import ValidationError


def validate_habit(data):
    """
    Валидация данных привычки.

    Аргументы:
        data: Данные привычки для валидации.
    """
    # Исключить одновременный выбор связанной привычки и указания вознаграждения
    if data.get('reward') and data.get('related_habit'):
        raise ValidationError("Нельзя указывать одновременно и вознаграждение, и связанную привычку.")

    # Время выполнения должно быть не больше 120 секунд
    execution_time = data.get('execution_time')
    if execution_time is not None and execution_time > 120:
        raise ValidationError("Время на выполнение не может быть больше 120 секунд.")

    # В связанные привычки могут попадать только привычки с признаком приятной привычки
    related_habit = data.get('related_habit')
    if related_habit and not related_habit.is_pleasant:
        raise ValidationError("Связанная привычка должна быть приятной привычкой.")

    # У приятной привычки не может быть вознаграждения или связанной привычки
    is_pleasant = data.get('is_pleasant')
    if is_pleasant and (data.get('reward') or related_habit):
        raise ValidationError("Приятная привычка не может иметь вознаграждение или связанную привычку.")

    # Нельзя выполнять привычку реже, чем 1 раз в 7 дней
    period = data.get('period')
    if period is not None and (period < 1 or period > 7):
        raise ValidationError("Периодичность выполнения должна быть от 1 до 7 дней.")
