from rest_framework.serializers import ModelSerializer, CharField
from django.contrib.auth.hashers import make_password
from users.models import User


class UserCreateSerializer(ModelSerializer):
    """
    Сериализатор для создания нового пользователя.
    """
    password = CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class UserUpdateSerializer(ModelSerializer):
    """
    Сериализатор для обновления существующего пользователя.
    """
    password = CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = '__all__'

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().update(instance, validated_data)


class UserProfileSerializer(ModelSerializer):
    """
    Сериализатор для модели User, исключающий поле password.
    """

    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'city', 'tg_nick', 'tg_chat_id']
