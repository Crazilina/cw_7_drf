from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from users.models import User
from users.serializers import UserCreateSerializer, UserUpdateSerializer, UserProfileSerializer


class UserViewSet(ModelViewSet):
    """
    ViewSet для выполнения CRUD операций над моделью User.
    """
    queryset = User.objects.all()

    def get_serializer_class(self):
        """
        Возвращает соответствующий сериализатор в зависимости от действия.

        - Для действия 'create' возвращает UserCreateSerializer.
        - Для действия 'retrieve' возвращает UserProfileSerializer.
        - Для действий 'update' и 'partial_update' возвращает UserUpdateSerializer.
        - Для всех остальных действий возвращает UserUpdateSerializer.
        """
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action == 'retrieve':
            return UserProfileSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserUpdateSerializer

    def get_permissions(self):
        """
        Возвращает соответствующие разрешения в зависимости от действия.

        - Для действия 'create' возвращает AllowAny для разрешения создания пользователя без аутентификации.
        - Для всех остальных действий возвращает IsAuthenticated для защиты действий аутентификацией.
        """
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        """
        Переопределяет метод сохранения для установки пароля пользователя и активации учетной записи.

        - Устанавливает пароль, используя set_password для сохранения пароля в зашифрованном виде.
        - Устанавливает is_active в True для активации учетной записи.
        """
        user = serializer.save(is_active=True)
        user.set_password(serializer.validated_data['password'])
        user.save()
