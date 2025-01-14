# user_profile/forms.py
from django import forms
from django.contrib.auth.models import User
#from user_profile.models import CustomUser
from .models import Profile

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio']

