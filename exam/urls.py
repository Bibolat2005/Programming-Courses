from django.urls import path
from . import views
from rest_framework.decorators import api_view
from .views import TakeTestView

urlpatterns = [
    #path('take_test/<slug:slug>/', views.take_test, name='take_test'),
    path('take_test/<slug:slug>/', TakeTestView.as_view(), name='take_test'),
    
]