from django.shortcuts import render, get_object_or_404, redirect
from courses.models import Course, Video
from .models import Question, UserAnswer, TestResult 
from django.contrib.auth.decorators import login_required
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import IsAuthenticated

class TakeTestView(APIView):
    permission_classes = [IsAuthenticated]

    lecture_param = openapi.Parameter(
        'lecture', openapi.IN_QUERY, description="Serial number of the lecture", type=openapi.TYPE_STRING
    )

    @swagger_auto_schema(manual_parameters=[lecture_param], responses={200: "Questions data"})
    def get(self, request, slug):
        course = get_object_or_404(Course, slug=slug)
        serial_number = request.GET.get('lecture')
        if not serial_number:
            return Response({"error": "Lecture serial number is required"}, status=400)

        video = get_object_or_404(Video, serial_number=serial_number, course=course)
        questions = video.questions.all()
        if not questions.exists():
            return Response({"error": "No questions available for this test."}, status=404)

        return Response({"questions": [{"id": q.id, "text": q.question_text} for q in questions]})

    @swagger_auto_schema(manual_parameters=[lecture_param], responses={200: "Test results or question data"})
    def post(self, request, slug):
        course = get_object_or_404(Course, slug=slug)
        serial_number = request.GET.get('lecture')
        if not serial_number:
            return Response({"error": "Lecture serial number is required"}, status=400)

        video = get_object_or_404(Video, serial_number=serial_number, course=course)
        questions = video.questions.all()

        score = 0
        total_questions = questions.count()
        for question in questions:
            selected_option = request.data.get(str(question.id))
            if selected_option:
                selected_option = int(selected_option)
                is_correct = selected_option == question.correct_option
                if is_correct:
                    score += 1

                UserAnswer.objects.create(
                    user=request.user,
                    question=question,
                    selected_option=selected_option,
                    is_correct=is_correct
                )

        test_result, created = TestResult.objects.update_or_create(
            user=request.user, video=video,
            defaults={"score": score, "total_questions": total_questions}
        )
        return Response({"score": score, "total_questions": total_questions})


@login_required
def take_test(request, slug):
    course = get_object_or_404(Course, slug=slug)
    serial_number = request.GET.get('lecture')
    if not serial_number:
        return redirect('course_page', slug=slug)

    video = get_object_or_404(Video, serial_number=serial_number, course=course)
    questions = video.questions.all()

    if not questions.exists():
        return render(request, 'exam/no_questions.html', {
            'video': video,
            'course': course,
            'error': "В тесте отсутствуют вопросы."
        })

    test_result = TestResult.objects.filter(user=request.user, video=video).first()

    if request.method == 'POST':
        score = 0
        total_questions = questions.count()

        for question in questions:
            selected_option = request.POST.get(str(question.id))
            if selected_option:
                selected_option = int(selected_option)
                is_correct = selected_option == question.correct_option

                if is_correct:
                    score += 1

                UserAnswer.objects.create(
                    user=request.user,
                    question=question,
                    selected_option=selected_option,
                    is_correct=is_correct
                )

        if test_result:
            test_result.score = score
            test_result.total_questions = total_questions
            test_result.save()
        else:
            TestResult.objects.create(
                user=request.user,
                video=video,
                score=score,
                total_questions=total_questions
            )

        return render(request, 'exam/results.html', {
            'score': score,
            'total': total_questions,
            'course': course
        })

    return render(request, 'exam/take_test.html', {
        'course': course,
        'video': video,
        'questions': questions,
        'test_result': test_result
    })
# @login_required
# def take_test(request, slug):
#     course = get_object_or_404(Course, slug=slug)
#     serial_number = request.GET.get('lecture')
#     if not serial_number:
#         return redirect('course_page', slug=slug)

#     video = get_object_or_404(Video, serial_number=serial_number, course=course)
#     questions = video.questions.all()

#     if not questions.exists():
#         return render(request, 'exam/no_questions.html', {
#             'video': video,
#             'course': course,
#             'error': "В тесте отсутствуют вопросы."
#         })


#     test_result = TestResult.objects.filter(user=request.user, video=video).first()

#     if request.method == 'POST':
#         score = 0
#         total_questions = questions.count()

#         for question in questions:
#             selected_option = request.POST.get(str(question.id))
#             if selected_option:
#                 selected_option = int(selected_option)
#                 is_correct = selected_option == question.correct_option

#                 if is_correct:
#                     score += 1


#                 UserAnswer.objects.create(
#                     user=request.user,
#                     question=question,
#                     selected_option=selected_option,
#                     is_correct=is_correct
#                 )

#         if test_result:
#             test_result.score = score
#             test_result.total_questions = total_questions
#             test_result.save()
#         else:
#             TestResult.objects.create(
#                 user=request.user,
#                 video=video,
#                 score=score,
#                 total_questions=total_questions
#             )

#         return render(request, 'exam/results.html', {
#             'score': score,
#             'total': total_questions,
#             'course': course
#         })

#     return render(request, 'exam/take_test.html', {
#         'course': course,
#         'video': video,
#         'questions': questions,
#         'test_result': test_result
#     })
