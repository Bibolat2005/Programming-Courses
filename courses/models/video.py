from django.db import models
from courses.models import Course
class Lesson(models.Model):
    title = models.CharField(max_length=200)
    # Другие поля для урока...

    def __str__(self):
        return self.title

class Video(models.Model):
    title = models.CharField(max_length = 100, null = False)
    course = models.ForeignKey(Course, null = False, on_delete = models.CASCADE)
    serial_number = models.IntegerField(null = False)
    video_id = models.CharField(max_length = 20, null = False)
    is_preview = models.BooleanField(default = False)
    video_url = models.CharField(max_length = 100, null = False) 

    def __str__(self):
        return self.title