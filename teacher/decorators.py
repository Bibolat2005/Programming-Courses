# teacher/decorators.py

from django.http import HttpResponseForbidden
from functools import wraps

# def teacher_required(view_func):
#     @wraps(view_func)
#     def _wrapped_view(request, *args, **kwargs):
#         if request.user.is_authenticated and hasattr(request.user, 'profile') and request.user.profile.role == 'teacher':
#             return view_func(request, *args, **kwargs)
#         return HttpResponseForbidden("You do not have permission to access this page.")
#     return _wrapped_view
