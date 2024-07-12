from django.urls import path
from rest_framework.routers import SimpleRouter

from habits.apps import HabitsConfig
from habits.views import (HabitListAPIView, HabitCreateAPIView, HabitRetrieveAPIView, HabitUpdateAPIView,
                          HabitDestroyAPIView)

app_name = HabitsConfig.name

router = SimpleRouter()

urlpatterns = [
    path('', HabitListAPIView.as_view(), name="habit-list"),
    path('create/', HabitCreateAPIView.as_view(), name="habit-create"),
    path('<int:pk>/', HabitRetrieveAPIView.as_view(), name="habit-retrieve"),
    path('<int:pk>/update/', HabitUpdateAPIView.as_view(), name="habit-update"),
    path('<int:pk>/delete/', HabitDestroyAPIView.as_view(), name="habit-delete"),
] + router.urls
