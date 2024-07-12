from rest_framework.serializers import ModelSerializer, ValidationError
from habits.models import Habit
from habits.validators import validate_habit


class HabitSerializer(ModelSerializer):
    """ Сериализатор для модели Habit."""

    class Meta:
        model = Habit
        fields = '__all__'
        read_only_fields = ['owner']

    def validate(self, data):
        """
        Переопределение метода validate для использования нашего валидатора.
        """
        validate_habit(data)
        return data
