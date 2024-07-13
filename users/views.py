from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from users.models import User
from users.serializers import UserCreateSerializer, UserUpdateSerializer, UserProfileSerializer
from drf_yasg.utils import swagger_auto_schema


class UserViewSet(ModelViewSet):
    """
    ViewSet для выполнения CRUD операций над моделью User.
    """
    queryset = User.objects.all()

    def get_serializer_class(self):
        """
        Возвращает соответствующий сериализатор в зависимости от действия.
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
        """
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]

    @swagger_auto_schema(
        operation_description="Создание нового пользователя",
        request_body=UserCreateSerializer,
        responses={201: UserCreateSerializer}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Получение данных пользователя по ID",
        responses={200: UserProfileSerializer}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Обновление данных пользователя по ID",
        request_body=UserUpdateSerializer,
        responses={200: UserUpdateSerializer}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Частичное обновление данных пользователя по ID",
        request_body=UserUpdateSerializer,
        responses={200: UserUpdateSerializer}
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Удаление пользователя по ID",
        responses={204: 'Нет содержимого'}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        """
        Переопределяет метод сохранения для установки пароля пользователя и активации учетной записи.
        """
        user = serializer.save(is_active=True)
        user.set_password(serializer.validated_data['password'])
        user.save()
