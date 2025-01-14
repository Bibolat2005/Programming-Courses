from django.db import models
from courses.models import Course
from django.contrib.auth.models import User
#from user_profile.models import CustomUser

class UserCourse(models.Model):
    user = models.ForeignKey(User, null = False, on_delete = models.CASCADE)
    course = models.ForeignKey(Course, null = False, on_delete = models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    grade = models.CharField(max_length=2, null=True, blank=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} - {self.course.name}'
    
class CourseMaterial(models.Model):
    course = models.ForeignKey(Course, related_name='materials', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='course_materials/')
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title