from django.db import models
from courses.models import Video
from django.contrib.auth.models import User
#from user_profile.models import CustomUser


class Question(models.Model):
    question_text = models.CharField(max_length=255)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='questions')

    option_1 = models.CharField(max_length=200)
    option_2 = models.CharField(max_length=200)
    option_3 = models.CharField(max_length=200)
    option_4 = models.CharField(max_length=200)
    correct_option = models.IntegerField(choices=[(1, 'Option 1'), (2, 'Option 2'), (3, 'Option 3'), (4, 'Option 4')])

    def __str__(self):
        return self.question_text

class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.IntegerField()
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} - {self.question.question_text}'
    
class TestResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    score = models.IntegerField()
    total_questions = models.IntegerField()
    passed = models.BooleanField(default=False) 
    date_taken = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f'{self.user.username} - {self.video.title} - {self.score}/{self.total_questions}'