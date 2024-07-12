from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from habits.models import Habit
from habits.serializers import HabitSerializer
from users.permissions import IsOwner


class HabitCreateAPIView(CreateAPIView):
    """
    Контроллер создания новой привычки.
    """
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Переопределяет метод создания объекта для привязки к авторизованному пользователю.
        """
        serializer.save(owner=self.request.user)


class HabitListAPIView(ListAPIView):
    """
    Контроллер для получения списка всех привычек текущего пользователя и публичных привычек.
    """
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Переопределяет queryset для фильтрации по текущему пользователю и публичным привычкам.
        """
        user = self.request.user
        return Habit.objects.filter(owner=user) | Habit.objects.filter(is_public=True)


class HabitRetrieveAPIView(RetrieveAPIView):
    """
    Контроллер для получения одной привычки текущего пользователя по указанному id.
    """
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        """
        Переопределяет queryset для фильтрации по текущему пользователю.
        """
        return self.queryset.filter(owner=self.request.user)


class HabitUpdateAPIView(UpdateAPIView):
    """
    Контроллер для обновления одной привычки текущего пользователя по указанному id.
    """
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        """
        Переопределяет queryset для фильтрации по текущему пользователю.
        """
        return self.queryset.filter(owner=self.request.user)


class HabitDestroyAPIView(DestroyAPIView):
    """
    Контроллер для удаления одной привычки текущего пользователя по указанному id.
    """
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        """
        Переопределяет queryset для фильтрации по текущему пользователю.
        """
        return self.queryset.filter(owner=self.request.user)
