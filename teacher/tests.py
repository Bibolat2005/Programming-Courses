from django.test import TestCase
from django.contrib.auth.models import User
#from user_profile.models import CustomUser
from teacher.models import Teacher
from courses.models import Course
from django.urls import reverse

class TeacherTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='teacher1', password='password123')
        self.teacher1 = Teacher.objects.create(user=self.user1, bio="Experienced teacher")
        self.course1 = Course.objects.create(name="Python Basics", description="Learn Python from scratch")
        self.teacher1.courses.add(self.course1)

        self.user2 = User.objects.create_user(username='teacher2', password='password456')
        self.teacher2 = Teacher.objects.create(user=self.user2, bio="Another teacher")
        self.course2 = Course.objects.create(name="Django Basics", description="Learn Django from scratch")
        self.teacher2.courses.add(self.course2)

    def test_teacher_courses(self):
        # Teacher1 should be able to access their own course
        self.client.login(username='teacher1', password='password123')
        response = self.client.get(reverse('teacher_courses'))
        self.assertContains(response, 'Python Basics')
        self.assertNotContains(response, 'Django Basics')

        # Teacher2 should be able to access their own course
        self.client.login(username='teacher2', password='password456')
        response = self.client.get(reverse('teacher_courses'))
        self.assertContains(response, 'Django Basics')
        self.assertNotContains(response, 'Python Basics')
