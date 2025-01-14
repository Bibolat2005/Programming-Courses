from django import forms
from .models import Teacher
from django.contrib.auth.models import User
#from user_profile.models import CustomUser
from courses.models import Course


class TeacherProfileForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['bio', 'courses']
        widgets = {
            'courses': forms.CheckboxSelectMultiple(),
        }

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'slug', 'description', 'price', 'discount', 'active',
            'thumbnail', 'resource', 'length', 'product_id']

# class AddStudentForm(forms.Form):
#     student = forms.ModelChoiceField(queryset=User.objects.all(), label="Student")
#     course = forms.ModelChoiceField(queryset=Course.objects.all(), label="Course")

#     def __init__(self, teacher, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['course'].queryset = teacher.courses.all()

class AddStudentForm(forms.Form):
    student = forms.ModelChoiceField(queryset=User.objects.all(), label="Student")
    course = forms.ModelChoiceField(queryset=Course.objects.all(), label="Course")

    def __init__(self, teacher, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Убедитесь, что teacher — это объект модели Teacher
        if teacher and isinstance(teacher, Teacher):
            self.fields['course'].queryset = teacher.courses.all()
        else:
            # Если teacher не передан или не является экземпляром Teacher, сделайте queryset пустым
            self.fields['course'].queryset = Course.objects.none()