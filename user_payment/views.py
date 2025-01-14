from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from courses.models import Course
from user_payment.models import UserPayment
import stripe
import time
from django.shortcuts import render, get_object_or_404
from django.db.models import Avg
from .models import Course, Review
from .forms import ReviewForm
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
from rest_framework.decorators import api_view

product_slug_param = openapi.Parameter(
    'slug', openapi.IN_PATH, description="The slug of the course", type=openapi.TYPE_STRING
)

# Add Swagger documentation to 'product_page'
# @swagger_auto_schema(
#     manual_parameters=[product_slug_param], 
#     responses={200: 'Course information', 400: 'Invalid request'}
# )


@login_required(login_url='login')

def product_page(request, slug):
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    course = Course.objects.get(slug=slug)
    has_purchased = UserPayment.objects.filter(app_user=request.user, course=course, payment_bool=True).exists()
	
    if has_purchased:
        return render(request, 'user_payment/already_purchased.html', {'course': course})

    if request.method == 'POST':
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price': course.product_id,
                    'quantity': 1,
                },
            ],
            mode='payment',
            customer_creation='always',
            success_url=settings.REDIRECT_DOMAIN + f'/payment_successful?session_id={{CHECKOUT_SESSION_ID}}&course_id={course.id}',
            cancel_url=settings.REDIRECT_DOMAIN + '/payment_cancelled',
        )
        return redirect(checkout_session.url, code=303)

    return render(request, 'user_payment/product_page.html', {'course': course})


@login_required(login_url='login')
def purchased_courses(request):
    purchased_courses = UserPayment.objects.filter(app_user=request.user, payment_bool=True).select_related('course')
    
    courses = [payment.course for payment in purchased_courses]
    reviews = {course.slug: Review.objects.filter(course=course) for course in courses}  # Получаем отзывы для каждого курса

    if request.method == 'POST':
        for course in courses:
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.user = request.user
                review.course = course
                review.save()
                return redirect('purchased_courses')  # Перенаправляем на ту же страницу после отправки

    forms = {course.slug: ReviewForm() for course in courses}  # Создаем формы для каждого курса

    return render(request, 'user_payment/purchased_courses.html', {
        'courses': courses,
        'reviews': reviews,
        'forms': forms,
    })

## use Stripe dummy card: 4242 4242 4242 4242
@swagger_auto_schema(
    method='get',  
    responses={200: 'Payment successful response', 400: 'Invalid request'}
)
@api_view(['GET'])
def payment_successful(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    checkout_session_id = request.GET.get('session_id')
    course_id = request.GET.get('course_id')
    
    session = stripe.checkout.Session.retrieve(checkout_session_id)
    customer = stripe.Customer.retrieve(session.customer)
    
    # Создаем запись о платеже
    course = Course.objects.get(id=course_id)
    UserPayment.objects.create(
        app_user=request.user,
        course=course,
        stripe_checkout_id=checkout_session_id,
        payment_bool=True
    )
    
    return render(request, 'courses/payment_successful.html', {'customer': customer})



def payment_cancelled(request):
	stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
	return render(request, 'courses/payment_cancelled.html')


# @swagger_auto_schema(
#     method='post',
#     responses={200: 'Webhook received successfully', 400: 'Bad request'}
# )
# @api_view(['POST'])
@csrf_exempt
def stripe_webhook(request):
	stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
	time.sleep(10)
	payload = request.body
	signature_header = request.META['HTTP_STRIPE_SIGNATURE']
	event = None
	try:
		event = stripe.Webhook.construct_event(
			payload, signature_header, settings.STRIPE_WEBHOOK_SECRET_TEST
		)
	except ValueError as e:
		return HttpResponse(status=400)
	except stripe.error.SignatureVerificationError as e:
		return HttpResponse(status=400)
	if event['type'] == 'checkout.session.completed':
		session = event['data']['object']
		session_id = session.get('id', None)
		time.sleep(15)
		user_payment = UserPayment.objects.get(stripe_checkout_id=session_id)
		user_payment.payment_bool = True
		user_payment.save()
	return HttpResponse(status=200)

@swagger_auto_schema(
    method='post',
    manual_parameters=[
        openapi.Parameter('course_slug', openapi.IN_PATH, description="Course slug", type=openapi.TYPE_STRING)
    ],
    responses={200: 'Review created successfully', 400: 'Invalid request'}
)

@login_required
@api_view(['POST'])
def create_review(request, course_slug):
    user_payment = get_object_or_404(UserPayment, app_user=request.user, course__slug=course_slug, payment_bool=True)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.course = user_payment.course
            review.user_payment = user_payment
            review.save()
            return redirect('purchased_courses') 
    else:
        form = ReviewForm()

    return render(request, 'user_payment/review_form.html', {'form': form, 'course': user_payment.course})

@login_required
def update_review(request, course_slug):
    review_id = request.GET.get('review_id')  
    reviews = Review.objects.filter(user=request.user, course__slug=course_slug)

    if review_id:
        review = get_object_or_404(Review, id=review_id, user=request.user)
    elif reviews.count() == 1:
        review = reviews.first()  
    else:
        return render(request, 'user_payment/select_review.html', {'reviews': reviews, 'course_slug': course_slug})

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('purchased_courses')
    else:
        form = ReviewForm(instance=review)

    return render(request, 'user_payment/review_form.html', {'form': form, 'course': review.course})

def review_list(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug)
    reviews = Review.objects.filter(course=course)
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg'] 
    average_rating = round(average_rating, 2) if average_rating else "No ratings yet"
    
    return render(request, 'user_payment/review_list.html', {
        'course': course,
        'reviews': reviews,
        'average_rating': average_rating,  
    })

@login_required
def delete_review(request, course_slug, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    course = get_object_or_404(Course, slug=course_slug)

    if request.method == 'POST':
        review.delete()
        return redirect('list_reviews', course_slug=course_slug) 

    return render(request, 'user_payment/review_confirm_delete.html', {'review': review, 'course': course})
