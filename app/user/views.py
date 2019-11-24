from user.serializers import UserSerializer
from rest_framework import generics


class CreateUserView(generics.CreateAPIView):
    """Create a user"""

    serializer_class = UserSerializer
