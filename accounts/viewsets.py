from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from accounts.serializers import UserSerializer


class RegisterView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        """
            Handle POST requests for user registration.
            Args:
                request (Request): HTTP POST request containing user data.
            Returns:
                Response: HTTP response with user data and status code.
            Raises:
                AuthenticationFailed: If user data is invalid.
        """
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request):
        """
            Handle POST requests for user login.
            Args:
                request (Request): HTTP POST request containing user credentials.
            Returns:
                Response: HTTP response with access token and status code.
            Raises:
                AuthenticationFailed: If user credentials are invalid.
        """
        username = request.data.get('username')
        password = request.data.get('password')

        user = get_user_model().objects.filter(username=username).first()

        if not user or not user.check_password(password):
            raise AuthenticationFailed("Invalid username or password")

        access_token = AccessToken.for_user(user)
        response = Response()
        response.data = {
            'access_token': str(access_token),
        }
        return response
