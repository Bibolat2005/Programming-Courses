from django.db import models
from django.contrib.auth.models import User
#from user_profile.models import CustomUser
from courses.models import Course


class UserPayment(models.Model):
    app_user = models.ForeignKey(User, on_delete=models.CASCADE)  # Пользователь может иметь несколько платежей
    course = models.ForeignKey(Course, on_delete=models.CASCADE, default=1)  # Связь с курсом
    stripe_checkout_id = models.CharField(max_length=255, null=True, blank=True)
    payment_bool = models.BooleanField(default=False)

    def __str__(self):
        return f'Payment info for {self.app_user.username} for course {self.course.title}'


    def __str__(self):
        return f'Payment info for {self.app_user.username} for course {self.course.title}'
    

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
    user_payment = models.ForeignKey(UserPayment, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=5)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} review on {self.course.title}'
