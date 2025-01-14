from django.shortcuts import render
from courses.models import Course
from django.shortcuts import HttpResponse


def home(request):
    courses = Course.objects.all()
    print(courses)
    return render(request, template_name="courses/home.html",
    context={"courses" : courses})