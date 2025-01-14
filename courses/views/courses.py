from django.shortcuts import get_object_or_404, render, redirect
from courses.models import Course, Video, UserCourse
from user_payment.models import UserPayment
from django.urls import reverse
from exam.models import TestResult
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from courses.serializers import CourseSerializer
from rest_framework.permissions import AllowAny

class CourseListView(APIView):
    def get(self, request):
        try:
            courses = Course.objects.all()
            serializer = CourseSerializer(courses, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@login_required(login_url='login')
def coursePage(request, slug):
    course = get_object_or_404(Course, slug=slug)
    serial_number = request.GET.get('lecture')

    videos = course.video_set.all().order_by("serial_number")

    if serial_number is None:
        serial_number = 1

    video = get_object_or_404(Video, serial_number=serial_number, course=course)
    user_course, created = UserCourse.objects.get_or_create(user=request.user, course=course)

    test_result = TestResult.objects.filter(user=request.user, video=video).first()

    user_payment = UserPayment.objects.filter(app_user=request.user, course=course, payment_bool=True).exists()

    if not user_payment and not video.is_preview:
        return redirect('product_page', slug=course.slug)

    context = {
        "course": course,
        "video": video,
        'videos': videos,
        'product_page_url': reverse('product_page', kwargs={'slug': course.slug}),
        'test_result': test_result,
        'user_course': user_course,
    }
    return render(request, template_name="courses/course_page.html", context=context)


@login_required
def final_test_page(request, slug):
    course = get_object_or_404(Course, slug=slug)
    user_course, created = UserCourse.objects.get_or_create(user=request.user, course=course)
    if user_course.completed:
        return redirect('course_page', slug=course.slug)
    questions = {}
    if course.name == "Python for Beginners":
        questions = {
            "What is a variable in Python?": ["A container for data", "A type of loop", "An error", "None of the above"],
            "What is a function?": ["A block of code", "A data type", "An operator", "None of the above"],
            "How do you declare a list in Python?": ["[]", "{}", "()", "<>"] ,
            "What is the difference between a list and a tuple?": ["Lists are mutable, tuples are not", "Tuples are mutable, lists are not", "They are the same", "None of the above"],
            "What is the purpose of the 'return' statement?": ["To exit a function and return a value", "To declare a variable", "To start a loop", "None of the above"],
            "What is Python?": ["A programming language", "A type of snake", "An IDE", "None of the above"],
            "Which of the following is a Python data type?": ["int", "for", "define", "None of the above"],
            "What keyword is used to create a function?": ["def", "function", "define", "None of the above"],
            "Which symbol is used for comments in Python?": ["#", "//", "/* */", "None of the above"],
            "What is the output of print(2 + 3)?": ["5", "23", "Error", "None of the above"]
        }
    elif course.name == "C++ for Beginners":
        questions = {
            "What is a pointer in C++?": ["A variable that stores memory address", "A data type", "An operator", "None of the above"],
            "What are constructors and destructors?": ["Special functions in classes", "Loop controls", "Variable types", "None of the above"],
            "How do you declare an array in C++?": ["int arr[10];", "list arr = []", "array arr{};", "None of the above"],
            "What is function overloading?": ["Using multiple functions with the same name but different parameters", "Using functions inside loops", "A function that calls itself", "None of the above"],
            "What is the purpose of header files?": ["To define functions and macros", "To write code", "To create classes", "None of the above"],
            "What is inheritance in C++?": ["A mechanism to create a new class from an existing class", "A loop", "A function", "None of the above"],
            "What is polymorphism?": ["Ability of a function to have multiple forms", "A data type", "A pointer", "None of the above"],
            "How do you define a class in C++?": ["class ClassName { }", "def ClassName() { }", "function ClassName() { }", "None of the above"],
            "Which operator is used to access members of a class?": [". (dot operator)", "* (asterisk)", "& (ampersand)", "None of the above"],
            "How do you comment a line in C++?": ["//", "#", "/* */", "None of the above"]
        }
    elif course.name == "JavaScript for beginners":
        questions = {
            "What is JavaScript used for?": ["Creating interactive web pages", "Server management", "Database handling", "None of the above"],
            "How do you declare a variable in JavaScript?": ["let", "int", "define", "None of the above"],
            "What is the difference between 'let' and 'var'?": ["'let' has block scope, 'var' does not", "'var' has block scope, 'let' does not", "They are the same", "None of the above"],
            "What is an event in JavaScript?": ["An action that happens in the browser", "A loop", "A variable", "None of the above"],
            "What is the purpose of 'this' keyword?": ["Refers to the current object", "Declares a function", "Starts a loop", "None of the above"],
            "Which symbol is used for comments in JavaScript?": ["//", "#", "/* */", "None of the above"],
            "What is the purpose of the 'for' loop?": ["To iterate over a sequence", "To create a function", "To declare a variable", "None of the above"],
            "What does DOM stand for?": ["Document Object Model", "Data Object Management", "Desktop Operating Machine", "None of the above"],
            "How do you write 'Hello World' in an alert box?": ["alert('Hello World')", "msg('Hello World')", "console.log('Hello World')", "None of the above"],
            "What is JSON?": ["JavaScript Object Notation", "Java System Object Naming", "Java Syntax Object Number", "None of the above"]
        }
    elif course.name == "React Framework":
        questions = {
            "What is React?": ["A JavaScript library for building user interfaces", "A database management tool", "A CSS framework", "None of the above"],
            "What is JSX?": ["A syntax extension for JavaScript", "A new programming language", "A CSS preprocessor", "None of the above"],
            "How do you create a component in React?": ["Using a function or a class", "Using HTML directly", "By creating a database", "None of the above"],
            "What is the virtual DOM?": ["A lightweight copy of the real DOM", "A CSS file", "A backend framework", "None of the above"],
            "What is the use of props in React?": ["To pass data between components", "To define styles", "To manage state", "None of the above"],
            "What is state in React?": ["An object that determines component rendering", "A function", "A CSS style", "None of the above"],
            "How do you handle events in React?": ["Using event handlers like onClick", "Using loops", "Using CSS", "None of the above"],
            "What is a React Hook?": ["A function that lets you use state and lifecycle features", "A CSS function", "A type of variable", "None of the above"],
            "How do you create a React app?": ["Using create-react-app command", "Using npm install", "By writing HTML", "None of the above"],
            "What is a higher-order component?": ["A function that takes a component and returns a new component", "A built-in component", "A CSS class", "None of the above"]
        }
    elif course.name == "Vue JS Framework":
        questions = {
            "What is Vue.js?": ["A progressive JavaScript framework", "A CSS library", "A database",
                                "None of the above"],
            "What is a Vue component?": ["A reusable instance with its own data and logic", "A CSS element",
                                         "A type of variable", "None of the above"],
            "How do you declare a Vue component?": ["Vue.component('component-name', {})", "var component = { }",
                                                    "function component() { }", "None of the above"],
            "What is a directive in Vue.js?": ["An instruction for the DOM", "A CSS selector", "A variable",
                                               "None of the above"],
            "What is the purpose of v-model?": ["To create two-way data binding", "To handle events",
                                                "To loop over elements", "None of the above"],
            "What is Vue Router?": ["A library for routing in Vue applications", "A CSS framework", "A database tool",
                                    "None of the above"],
            "What is the Vue CLI?": ["A command-line tool to create and manage Vue projects", "A CSS preprocessor",
                                     "A JavaScript library", "None of the above"],
            "What is a single-file component?": ["A Vue component in one .vue file", "A JavaScript module",
                                                 "A CSS file", "None of the above"],
            "How do you handle events in Vue?": ["Using v-on or @", "Using eventListener", "Using a CSS class",
                                                 "None of the above"],
            "What is the purpose of Vuex?": ["To manage state in Vue applications", "To style components",
                                             "To handle HTTP requests", "None of the above"]
        }
    elif course.name == "Unity Development":
        questions = {
            "What is Unity?": ["A game development platform", "A web server", "A type of database",
                               "None of the above"],
            "Which programming language is primarily used in Unity?": ["C#", "JavaScript", "Python",
                                                                       "None of the above"],
            "What is a GameObject in Unity?": ["An object that represents characters, props, and scenery", "A variable",
                                               "A script", "None of the above"],
            "What is the purpose of a script in Unity?": ["To control the behavior of GameObjects", "To style the game",
                                                          "To create textures", "None of the above"],
            "How do you add physics to an object in Unity?": ["Using Rigidbody component", "Using CSS",
                                                              "By adding JavaScript", "None of the above"],
            "What is the Unity Asset Store?": ["A marketplace for assets like 3D models and scripts", "A storage tool",
                                               "A game engine", "None of the above"],
            "What is a prefab in Unity?": ["A reusable GameObject", "A script", "A texture", "None of the above"],
            "How do you detect collisions in Unity?": ["Using OnCollisionEnter method", "Using event handlers",
                                                       "Using CSS selectors", "None of the above"],
            "What is the purpose of the Update() method?": ["To run code every frame", "To initialize variables",
                                                            "To stop the game", "None of the above"],
            "How do you make an object move in Unity?": ["By changing its Transform position", "By writing HTML",
                                                         "Using CSS animations", "None of the above"]
        }

    if request.method == 'POST':
        correct_answers = {
            "What is a variable in Python?": "A container for data",
            "What is a function?": "A block of code",
            "How do you declare a list in Python?": "[]",
            "What is the difference between a list and a tuple?": "Lists are mutable, tuples are not",
            "What is the purpose of the 'return' statement?": "To exit a function and return a value",
            "What is Python?": "A programming language",
            "Which of the following is a Python data type?": "int",
            "What keyword is used to create a function?": "def",
            "Which symbol is used for comments in Python?": "#",
            "What is the output of print(2 + 3)?": "5",
            "What is a pointer in C++?": "A variable that stores memory address",
            "What are constructors and destructors?": "Special functions in classes",
            "How do you declare an array in C++?": "int arr[10];",
            "What is function overloading?": "Using multiple functions with the same name but different parameters",
            "What is the purpose of header files?": "To define functions and macros",
            "What is inheritance in C++?": "A mechanism to create a new class from an existing class",
            "What is polymorphism?": "Ability of a function to have multiple forms",
            "How do you define a class in C++?": "class ClassName { }",
            "Which operator is used to access members of a class?": ". (dot operator)",
            "How do you comment a line in C++?": "//",
            "What is JavaScript used for?": "Creating interactive web pages",
            "How do you declare a variable in JavaScript?": "let",
            "What is the difference between 'let' and 'var'?": "'let' has block scope, 'var' does not",
            "What is an event in JavaScript?": "An action that happens in the browser",
            "What is the purpose of 'this' keyword?": "Refers to the current object",
            "Which symbol is used for comments in JavaScript?": "//",
            "What is the purpose of the 'for' loop?": "To iterate over a sequence",
            "What does DOM stand for?": "Document Object Model",
            "How do you write 'Hello World' in an alert box?": "alert('Hello World')",
            "What is JSON?": "JavaScript Object Notation",
            "What is React?": "A JavaScript library for building user interfaces",
            "What is JSX?": "A syntax extension for JavaScript",
            "How do you create a component in React?": "Using a function or a class",
            "What is the virtual DOM?": "A lightweight copy of the real DOM",
            "What is the use of props in React?": "To pass data between components",
            "What is state in React?": "An object that determines component rendering",
            "How do you handle events in React?": "Using event handlers like onClick",
            "What is a React Hook?": "A function that lets you use state and lifecycle features",
            "How do you create a React app?": "Using create-react-app command",
            "What is a higher-order component?": "A function that takes a component and returns a new component",
            "What is Vue.js?": "A progressive JavaScript framework",
            "What is a Vue component?": "A reusable instance with its own data and logic",
            "How do you declare a Vue component?": "Vue.component('component-name', {})",
            "What is a directive in Vue.js?": "An instruction for the DOM",
            "What is the purpose of v-model?": "To create two-way data binding",
            "What is Vue Router?": "A library for routing in Vue applications",
            "What is the Vue CLI?": "A command-line tool to create and manage Vue projects",
            "What is a single-file component?": "A Vue component in one .vue file",
            "How do you handle events in Vue?": "Using v-on or @",
            "What is the purpose of Vuex?": "To manage state in Vue applications",
            "What is Unity?": "A game development platform",
            "Which programming language is primarily used in Unity?": "C#",
            "What is a GameObject in Unity?": "An object that represents characters, props, and scenery",
            "What is the purpose of a script in Unity?": "To control the behavior of GameObjects",
            "How do you add physics to an object in Unity?": "Using Rigidbody component",
            "What is the Unity Asset Store?": "A marketplace for assets like 3D models and scripts",
            "What is a prefab in Unity?": "A reusable GameObject",
            "How do you detect collisions in Unity?": "Using OnCollisionEnter method",
            "What is the purpose of the Update() method?": "To run code every frame",
            "How do you make an object move in Unity?": "By changing its Transform position"
        }
        score = 0
        for index, question in enumerate(questions.keys(), 1):
            user_answer = request.POST.get(f'answer_{index}')
            if user_answer == correct_answers.get(question):
                score += 10

        if score >= 70:
            user_course.completed = True
            user_course.save()

            return redirect('course_page', slug=course.slug)
        else:
            context = {
                'course': course,
                'questions': questions,
                'error_message': 'You have not scored the minimum score (70). Try again.'
            }
            return render(request, 'courses/final_test.html', context)

    context = {
        'course': course,
        'questions': questions
    }
    return render(request, 'courses/final_test.html', context)