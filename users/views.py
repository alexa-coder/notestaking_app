# users/views.py
from rest_framework import generics, permissions
from .serializers import UserSerializer
from .models import User

class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]