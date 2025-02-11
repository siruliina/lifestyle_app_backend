from rest_framework import generics
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from datetime import timedelta
from django.conf import settings
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken

class RegisterUserView(generics.CreateAPIView):
    serializer_class = UserSerializer  # Associating the view with the UserSerializer
    permission_classes = [AllowAny]  # Token is not required when signing up

class LoginUserView(TokenObtainPairView):
    permission_classes = [AllowAny]  # Allowing all users to access this view
    authentication_classes = []  # We don't require authentication to get the token (login)

    def post(self, request, *args, **kwargs):
        # Get username and password from the request
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            raise AuthenticationFailed("Username and password are required")

        # Try to authenticate the user, if user exists a User object is put to user
        user = authenticate(request, username=username, password=password)

        if user is None:
            raise AuthenticationFailed("Invalid username or password")

        # Create JWT tokens for the authenticated user
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        # Set the tokens as cookies
        response = Response({
            "message": "Login successful.",
            "user_id": user.id,
            "access_token": access_token
        })

        # response.set_cookie(
        #     key='access_token',
        #     value=access_token,
        #     max_age=timedelta(minutes=5),
        #     httponly=False,
        #     secure=settings.SECURE_COOKIES,
        #     samesite='Lax'
        # )

        response.set_cookie(
            key='refresh_token',
            value=refresh_token,
            max_age=timedelta(days=7),
            httponly=True,
            secure=settings.SECURE_COOKIES,
            samesite='Lax'
        )

        return response

class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # Get refresh token from cookies
        refresh_token = request.COOKIES.get('refresh_token')

        if not refresh_token:
            return Response({"detail": "Refresh token not found in cookies."}, status=status.HTTP_400_BAD_REQUEST)

        request.data['refresh'] = refresh_token

        # Call the original `post` method to get the new access token
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200 and 'access' in response.data:
            # Decode the access token to get user id
            access_token = response.data['access']
            decoded_token = AccessToken(access_token)
            user_id = decoded_token.get('user_id')

            # Add user_id to the response
            response.data['user_id'] = user_id

        return response