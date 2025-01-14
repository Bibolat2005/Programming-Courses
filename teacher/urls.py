from django.urls import path
from . import views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('edit-profile/', views.edit_teacher_profile, name='edit_teacher_profile'),
    path('manage-courses/', views.manage_courses, name='manage_courses'),
    path('courses/', views.teacher_courses, name='teacher_courses'),
    path('create_course/', views.create_course, name='create_course'),
    path('courses/', views.teacher_courses, name='teacher_courses'), 
    path('course/<int:course_id>/stats/', views.course_students_stats, name='course_students_stats'), 
    path('add_student/', views.add_student_to_course, name='add_student_to_course'), 
    path('remove_student/<int:student_id>/<int:course_id>/', views.remove_student_from_course, name='remove_student_from_course'),
    path('upload_material/<int:course_id>/', views.upload_course_material, name='upload_course_material'),
    

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
