from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from ..models import User
from ..serializers import UserSerializer


class LoginView(APIView): 
    def post(self, request, action, id=None, instance=None):
        actions = {
            "authenticate-user" : self.authenticate_user, 
        }
        func = actions.get(action)
        if not func:
            return Response(
                {"message": "invalid action"},
                status=status.HTTP_400_BAD_REQUEST
            )
        return func(request, id=id, instance=instance)
    
    def authenticate_user(self, request, id=None, instance=None):
        username = request.data.get("username")
        password = request.data.get("password")

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"message": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)

        if not check_password(password, user.password):
            return Response({"message": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)

        # Generate JWT token
        refresh = RefreshToken.for_user(user)
        serializer = UserSerializer(user)


        # Detect profile
        student_id = None
        teacher_id = None

        if hasattr(user, "student_profile"):
            student_id = user.student_profile.id

        if hasattr(user, "teacher_profile"):
            teacher_id = user.teacher_profile.id
        return Response({
            "user" : serializer.data, 
            "student_id": student_id,
            "teacher_id": teacher_id,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        })