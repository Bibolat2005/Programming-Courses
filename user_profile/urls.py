# user_profile/urls.py
from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('get_cert/<str:course_name>/<int:user_id>/', views.get_certificate, name='get_certificate'),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
