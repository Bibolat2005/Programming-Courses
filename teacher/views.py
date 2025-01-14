from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from courses.serializers import AddStudentSerializer, CourseCreateSerializer, CourseMaterialSerializer, CourseSerializer
from .models import Teacher
from .forms import AddStudentForm, CourseForm, TeacherProfileForm
from courses.models import UserCourse, Course
from courses.forms.course_material_form import CourseMaterialForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from rest_framework import viewsets
from .serializers import TeacherSerializer
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import logging
from django.utils.text import slugify

logger = logging.getLogger(__name__)
# class TeacherView(APIView):
#     permission_classes = [IsAuthenticated]

#     @swagger_auto_schema(
#         responses={200: TeacherSerializer(many=False)},
#         operation_description="Fetch teacher's profile."
#     )
#     def get(self, request, *args, **kwargs):
#         teacher = get_object_or_404(Teacher, user=request.user)
#         serializer = TeacherSerializer(teacher)
#         return Response(serializer.data, status=status.HTTP_200_OK)
@login_required
@swagger_auto_schema(
    method='get',
    responses={200: openapi.Response('Teacher Dashboard', schema=TeacherSerializer(many=False))},
    operation_description="Render teacher's dashboard with basic profile info"
)
@api_view(['GET'])
def teacher_dashboard(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    return render(request, 'teacher/dashboard.html', {'teacher': teacher})


@login_required
@swagger_auto_schema(
    method='put',
    responses={200: openapi.Response('Edit Teacher Profile', schema=TeacherSerializer)},
    operation_description="Edit teacher profile information"
)
@api_view(['GET','PUT'])
def edit_teacher_profile(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    if request.method == 'POST':
        form = TeacherProfileForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            return redirect('teacher_dashboard')
    else:
        form = TeacherProfileForm(instance=teacher)
    return render(request, 'teacher/edit_profile.html', {'form': form})


@login_required
@swagger_auto_schema(
    method='get',
    # request_body=CourseSerializer,
    responses={200: openapi.Response('Manage Courses', schema=openapi.Schema(
        type=openapi.TYPE_ARRAY,
        items=openapi.Items(type=openapi.TYPE_OBJECT, properties={
            'course_id': openapi.Items(type=openapi.TYPE_INTEGER),
            'course_name': openapi.Items(type=openapi.TYPE_STRING),
        })
    ))},
    operation_description="Render teacher's dashboard with courses list"
)
@api_view(['GET'])
def manage_courses(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    courses = teacher.courses.all()
    return render(request, 'teacher/manage_courses.html', {'courses': courses})


@swagger_auto_schema(
    method='get',
    # request_body=CourseSerializer,
    responses={200: openapi.Response('Teacher Courses', schema=openapi.Schema(
        type=openapi.TYPE_ARRAY,
        items=openapi.Items(type=openapi.TYPE_OBJECT, properties={
            'course_id': openapi.Items(type=openapi.TYPE_INTEGER),
            'course_name': openapi.Items(type=openapi.TYPE_STRING),
        })
    ))},
    operation_description="View all courses taught by the teacher"
)
@api_view(['GET'])
def teacher_courses(request):
    teacher = Teacher.objects.get(user=request.user)
    courses = teacher.courses.all()
    return render(request, 'teacher/teacher_courses.html', {'courses': courses})

@swagger_auto_schema(
    method='get',
    # request_body=CourseSerializer,
    responses={200: openapi.Response('Course Students Stats', schema=openapi.Schema(
        type=openapi.TYPE_ARRAY,
        items=openapi.Items(type=openapi.TYPE_OBJECT, properties={
            'student': openapi.Items(type=openapi.TYPE_STRING),
            'grade': openapi.Items(type=openapi.TYPE_STRING),
            'completion_date': openapi.Items(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME),
        })
    ))},
    operation_description="Get student stats for a course"
)
@api_view(['GET'])
def course_students_stats(request, course_id):
    course = Course.objects.get(id=course_id) 
    students = UserCourse.objects.filter(course=course) 
    stats = [{'student': student.user.username, 'grade': student.grade, 'completion_date': student.date} for student in students]
    return render(request, 'teacher/course_stats.html', {'course': course, 'stats': stats})

@swagger_auto_schema(
    method='post',
    # request_body=AddStudentSerializer,
    responses={200: openapi.Response('Student Added to Course')},
    operation_description="Add a student to a course"
)
@api_view(['GET','POST'])
def add_student_to_course(request):
    teacher = Teacher.objects.get(user=request.user)
    if request.method == 'POST':
        form = AddStudentForm(teacher, request.POST)
        if form.is_valid():
            student = form.cleaned_data['student']
            course = form.cleaned_data['course']
            UserCourse.objects.create(user=student, course=course)
            return redirect('teacher_courses')
    else:
        form = AddStudentForm(teacher)
    return render(request, 'teacher/add_student_to_course.html', {'form': form})


@login_required
@swagger_auto_schema(
    method='delete',
    responses={200: openapi.Response('Student Removed from Course')},
    operation_description="Remove a student from a course"
)
@api_view(['DELETE'])
def remove_student_from_course(request, student_id, course_id):
    teacher = Teacher.objects.get(user=request.user)
    course = get_object_or_404(Course, id=course_id)
    student = get_object_or_404(User, id=student_id)
    
    if student in course.users.all():
        UserCourse.objects.filter(user=student, course=course).delete()
    
    return redirect('teacher_courses')


@login_required
@swagger_auto_schema(
    method='post',
    # request_body=CourseMaterialSerializer,
    responses={200: openapi.Response('Course Material Uploaded')},
    operation_description="Upload material to a course"
)
@api_view(['POST'])
@login_required
def upload_course_material(request, course_id):
    teacher = Teacher.objects.get(user=request.user) 
    course = Course.objects.get(id=course_id)  

    if request.method == 'POST':
        form = CourseMaterialForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.course = course 
            material.save()
            return redirect('course_details', course_id=course.id)  
    else:
        form = CourseMaterialForm()

    return render(request, 'teacher/upload_course_material.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def form_valid(self, form):
        user = form.get_user()
        if hasattr(user, 'teacher_profile'):
            return redirect('teacher_dashboard') 
        return super().form_valid(form)


@login_required  
@swagger_auto_schema(
    method='post',
    request_body=CourseCreateSerializer,
    responses={201: openapi.Response('Course Created')},
    operation_description="Create a new course"
)
@api_view(['GET','POST'])

# def create_course(request):
#     if request.method == 'POST':
#         form = CourseForm(request.POST)
#         if form.is_valid():
#             course = form.save(commit=False)
#             course.teacher = request.user  
#             course.save()
#             return redirect('course_list')
#     else:
#         form = CourseForm()
#     return render(request, 'teacher/create_course.html', {'form': form})

def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                course = form.save(commit=False)
                course.teacher = request.user
                if not course.slug:
                    course.slug = slugify(course.name)
                course.save()
                logger.info(f"Course created: {course.name}")
                return redirect(' ')
            except Exception as e:
                logger.error(f"Error creating course: {e}")
        else:
            logger.warning(f"Form is invalid: {form.errors}")
    form = CourseForm()
    return render(request, 'teacher/create_course.html', {'form': form})
# def create_course(request):
#     if request.method == 'POST':
#         form = CourseForm(request.POST, request.FILES)
        
#         if form.is_valid():
#             course = form.save(commit=False)
#             course.teacher = request.user
#             course.save()
            
#             return redirect('')
        
#         return render(request, 'teacher/create_course.html', {'form': form,'errors': form.errors})
#     else:
#         form = CourseForm()
#     return render(request, 'teacher/create_course.html', {'form': form})

# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from .models import Teacher
# from .forms import AddStudentForm, CourseForm
# from .forms import TeacherProfileForm
# from courses.models import UserCourse,Course
# from courses.forms.course_material_form import CourseMaterialForm
# from django.contrib.auth.models import User
# #from user_profile.models import CustomUser
# from courses.models.user_course import CourseMaterial
# from django.contrib.auth.views import LoginView
# from django.contrib.auth import login
# #from .decorators import teacher_required
# from rest_framework import viewsets
# from .serializers import TeacherSerializer
# from rest_framework.decorators import action
# from drf_yasg.utils import swagger_auto_schema
# from drf_yasg import openapi
# from rest_framework.decorators import api_view

# class TeacherViewSet(viewsets.ModelViewSet):
#     queryset = Teacher.objects.all()
#     serializer_class = TeacherSerializer

# @swagger_auto_schema(
#     operation_description="Teacher dashboard",
#     responses={200: openapi.Response('Teacher Dashboard')}
# )
# @login_required

# def teacher_dashboard(request):
#     teacher = get_object_or_404(Teacher, user=request.user)
#     return render(request, 'teacher/dashboard.html', {'teacher': teacher})

# @login_required
# @swagger_auto_schema(
#     operation_description="Edit teacher profile",
#     request_body=TeacherProfileForm,
#     responses={200: openapi.Response('Profile updated')}
# )
# def edit_teacher_profile(request):
#     teacher = get_object_or_404(Teacher, user=request.user)
#     if request.method == 'POST':
#         form = TeacherProfileForm(request.POST, instance=teacher)
#         if form.is_valid():
#             form.save()
#             return redirect('teacher_dashboard')
#     else:
#         form = TeacherProfileForm(instance=teacher)
#     return render(request, 'teacher/edit_profile.html', {'form': form})

# @login_required
# @swagger_auto_schema(
#     operation_description="Manage courses",
#     responses={200: openapi.Response('List of courses managed by teacher', schema=openapi.Schema(type=openapi.TYPE_OBJECT))}
# )
# def manage_courses(request):
#     teacher = get_object_or_404(Teacher, user=request.user)
#     courses = teacher.courses.all()
#     return render(request, 'teacher/manage_courses.html', {'courses': courses})

# @swagger_auto_schema(
#     operation_description="Get a list of courses taught by a teacher",
#     responses={200: openapi.Response('List of teacher courses', schema=openapi.Schema(type=openapi.TYPE_OBJECT))}
# )
# def teacher_courses(request):
#     teacher = Teacher.objects.get(user=request.user)
    
#     courses = teacher.courses.all()

#     return render(request, 'teacher/teacher_courses.html', {'courses': courses})

# # def create_course(request):
# #     if request.method == 'POST':
# #         form = CourseForm(request.POST)
# #         if form.is_valid():
# #             course = form.save(commit=False)
# #             teacher = request.user.teacher
# #             course.save()
# #             teacher.courses.add(course)
# #             return redirect('teacher_courses')
# #     else:
# #         form = CourseForm()

# #     return render(request, 'teacher/create_course.html', {'form': form})
# @swagger_auto_schema(
#     operation_description="Get students and stats for a particular course",
#     responses={200: openapi.Response('Course students stats', schema=openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_OBJECT)))}
# )
# def course_students_stats(request, course_id):
#     course = Course.objects.get(id=course_id) 
#     students = UserCourse.objects.filter(course=course) 
#     stats = [{'student': student.user.username, 'grade': student.grade, 'completion_date': student.date} for student in students]

#     return render(request, 'teacher/course_stats.html', {'course': course, 'stats': stats})

# @swagger_auto_schema(
#     operation_description="Add a student to a course",
#     request_body=AddStudentForm,
#     responses={200: openapi.Response('Student added to course')}
# )
# def add_student_to_course(request):
#     teacher = Teacher.objects.get(user=request.user)
    
#     if request.method == 'POST':
#         form = AddStudentForm(teacher, request.POST)
#         if form.is_valid():
#             student = form.cleaned_data['student']
#             course = form.cleaned_data['course']
            
            
#             UserCourse.objects.create(user=student, course=course)
#             return redirect('teacher_courses') 
#     else:
#         form = AddStudentForm(teacher)

#     return render(request, 'teacher/add_student_to_course.html', {'form': form})

# @login_required
# @swagger_auto_schema(
#     operation_description="Remove a student from a course",
#     responses={200: openapi.Response('Student removed from course')}
# )
# def remove_student_from_course(request, student_id, course_id):
#     teacher = Teacher.objects.get(user=request.user)
#     course = get_object_or_404(Course, id=course_id)
#     student = get_object_or_404(User, id=student_id)
    
#     if student in course.users.all():
#         UserCourse.objects.filter(user=student, course=course).delete()
    
#     return redirect('teacher_courses')

# @login_required
# @swagger_auto_schema(
#     operation_description="Upload course material for a course",
#     request_body=CourseMaterialForm,
#     responses={200: openapi.Response('Course material uploaded')}
# )
# def upload_course_material(request, course_id):
#     teacher = Teacher.objects.get(user=request.user) 
#     course = Course.objects.get(id=course_id)  

#     if request.method == 'POST':
#         form = CourseMaterialForm(request.POST, request.FILES)
#         if form.is_valid():
#             material = form.save(commit=False)
#             material.course = course 
#             material.save()
#             return redirect('course_details', course_id=course.id)  
#     else:
#         form = CourseMaterialForm()

#     return render(request, 'teacher/upload_course_material.html', {'form': form})

# class CustomLoginView(LoginView):
#     template_name = 'registration/login.html'

#     def form_valid(self, form):
        
#         user = form.get_user()

        
#         if hasattr(user, 'teacher_profile'):
#             return redirect('teacher_dashboard') 

#         return super().form_valid(form)

# @login_required  
# #@teacher_required
# @swagger_auto_schema(
#     operation_description="Create a new course",
#     request_body=CourseForm,
#     responses={200: openapi.Response('Course created')}
# )
# def create_course(request):
#     if request.method == 'POST':
#         form = CourseForm(request.POST)
#         if form.is_valid():
#             course = form.save(commit=False)
#             course.teacher = request.user  
#             course.save()
#             return redirect('course_list')
#     else:
#         form = CourseForm()
#     return render(request, 'teacher/create_course.html', {'form': form})