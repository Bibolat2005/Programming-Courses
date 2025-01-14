# serializers.py
from rest_framework import serializers
from .models import Course
from django.contrib.auth.models import User  # Импорт модели User, если она стандартная
from .models import Course, CourseMaterial

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'price']

class AddStudentSerializer(serializers.Serializer):
    student = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())

class CourseMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseMaterial  # Предполагаем, что у вас есть такая модель для материалов
        fields = ['id', 'course', 'file', 'description']

class CourseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['name', 'description', 'price']