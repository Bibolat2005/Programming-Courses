from django.db import models
from django.contrib.auth.models import User
#from user_profile.models import CustomUser
from courses.models import Course

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    bio = models.TextField(null=True, blank=True)
    courses = models.ManyToManyField(Course, related_name='teachers')

    def __str__(self):
        return self.user.username

