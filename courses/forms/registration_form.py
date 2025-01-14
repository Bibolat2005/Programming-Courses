from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
#from user_profile.models import CustomUser
from django import forms
from django.forms import ValidationError
class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=20, required= True)
    last_name = forms.CharField(max_length=20, required= True)
    email = forms.EmailField(max_length=25, required= True)

    class Meta:
        model = User
        fields = ['first_name'
                  , 'last_name', 'username'
                  ,"email", 'password1', 'password2']
    
def clean_email(self):
    email = self.cleaned_data['email']
    try:
        User.objects.get(email=email)
        raise ValidationError("User with this email already exists.")
    except User.DoesNotExist:
        return email


