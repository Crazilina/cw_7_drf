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
    if data.get('execution_time') > 120:
        raise ValidationError("Время на выполнение не может быть больше 120 секунд.")

    # В связанные привычки могут попадать только привычки с признаком приятной привычки
    if data.get('related_habit') and not data['related_habit'].is_pleasant:
        raise ValidationError("Связанная привычка должна быть приятной привычкой.")

    # У приятной привычки не может быть вознаграждения или связанной привычки
    if data.get('is_pleasant') and (data.get('reward') or data.get('related_habit')):
        raise ValidationError("Приятная привычка не может иметь вознаграждение или связанную привычку.")

    # Нельзя выполнять привычку реже, чем 1 раз в 7 дней
    if data.get('period') < 1 or data.get('period') > 7:
        raise ValidationError("Периодичность выполнения должна быть от 1 до 7 дней.")
