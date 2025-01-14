from django.urls import path
from . import views

urlpatterns = [
    path('product_page/<slug>/', views.product_page, name='product_page'),
    path('purchased_courses/', views.purchased_courses, name='purchased_courses'),
    path('payment_successful', views.payment_successful, name='payment_successful'),
    path('payment_cancelled', views.payment_cancelled, name='payment_cancelled'),
    path('stripe_webhook', views.stripe_webhook, name='stripe_webhook'),
    path('review/create/<slug:course_slug>/', views.create_review, name='create_review'),
    path('review/update/<slug:course_slug>/', views.update_review, name='update_review'),
    path('review/delete/<slug:course_slug>/<int:review_id>/', views.delete_review, name='delete_review'),
    path('review/list/<slug:course_slug>/', views.review_list, name='list_reviews'),
]
