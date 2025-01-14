from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
#from user_profile.models import CustomUser
from project.user_payment.models import UserPayment


@receiver(post_save, sender=User)
def create_user_payment(sender, instance, created, **kwargs):
    if created:
        UserPayment.objects.create(app_user=instance)

@receiver(post_save, sender=User)
def save_user_payment(sender, instance, **kwargs):
    instance.userpayment.save()