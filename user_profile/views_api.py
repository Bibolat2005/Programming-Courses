# # user_profile/views_api.py
# from rest_framework import viewsets
# from rest_framework.permissions import IsAuthenticated
# from rest_framework_simplejwt.authentication import JWTAuthentication
# from .models import Profile
# from .serializers import ProfileSerializer

# class ProfileViewSet(viewsets.ModelViewSet):
#     queryset = Profile.objects.all()
#     serializer_class = ProfileSerializer
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     def perform_create(self, serializer):
#         # Если нужно, можно добавить кастомную логику для создания профиля
#         serializer.save(user=self.request.user)
