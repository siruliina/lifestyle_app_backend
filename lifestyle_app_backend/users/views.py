from rest_framework.permissions import AllowAny
from rest_framework import status, generics
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.conf import settings
from datetime import timedelta

class RegisterUserView(generics.CreateAPIView):
    serializer_class = UserSerializer # Associating the view with the UserSerializer
    permission_classes = [AllowAny] # Token is not required when signing up

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        # Call the default post method to get the token pair
        response = super().post(request, *args, **kwargs)
        
        # Get the tokens from the response data
        access_token = response.data['access']
        refresh_token = response.data['refresh']

        # Set the tokens as cookies
        response.set_cookie(
            key='access_token',
            value=access_token,
            max_age=timedelta(minutes=5),
            httponly=False,  # Make it accessible to JavaScript
            secure=settings.SECURE_COOKIES,  # Set to True in production
            samesite='Lax'  # Can be 'Strict' or 'Lax'
        )

        response.set_cookie(
            key='refresh_token',
            value=refresh_token,
            max_age=timedelta(days=7),  # Customize the refresh token expiry time
            httponly=True,  # Make it inaccessible to JavaScript
            secure=settings.SECURE_COOKIES,  # Set to True in production
            samesite='Lax'  # Can be 'Strict' or 'Lax'
        )

        # Now we don't send the tokens back in the body
        response.data = {"message": "Login successful, tokens set in cookies."}
        return response