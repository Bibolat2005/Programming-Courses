# teacher/admin.py
from django.contrib import admin
from .models import Teacher
from courses.models import Course

# Регистрируем модель Teacher в админке
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')  # Показать user и bio в админке
    filter_horizontal = ('courses',)  # Отображение Many-to-Many поля

# Регистрируем модель Course в админке
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'teacher')  # Добавить отображение учителя
    search_fields = ('name', 'description')  # Поиск по названию и описанию курса
    list_filter = ('teacher',)  # Фильтрация по учителю


