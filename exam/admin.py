# exam/admin.py
from django.contrib import admin
from .models import  Question



class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'video', 'correct_option')
    fields = ['question_text', 'video', 'option_1', 'option_2', 'option_3', 'option_4', 'correct_option']

admin.site.register(Question, QuestionAdmin)

