from django.contrib import admin
from .models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('action', 'time', 'place', 'is_pleasant', 'period', 'execution_time', 'is_public')
    search_fields = ('action', 'place')
