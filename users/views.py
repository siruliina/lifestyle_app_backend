from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.conf import settings

from .serializers import UserSerializer, ChangePasswordSerializer
from datetime import timedelta

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from drf_spectacular.utils import extend_schema, OpenApiResponse


class RegisterUserView(generics.CreateAPIView):
    serializer_class = UserSerializer  # Associating the view with the UserSerializer
    permission_classes = [AllowAny]  # Token is not required when signing up


class LoginUserView(TokenObtainPairView):
    permission_classes = [AllowAny]  # Allowing all users to access this view
    authentication_classes = (
        []
    )  # We don't require authentication to get the token (login)

    def post(self, request, *args, **kwargs):
        # Get username and password from the request
        username = request.data.get("username")
        password = request.data.get("password")

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
        response = Response(
            {
                "message": "Login successful.",
                "user_id": user.id,
                "access_token": access_token,
            }
        )

        # response.set_cookie(
        #     key='access_token',
        #     value=access_token,
        #     max_age=timedelta(minutes=5),
        #     httponly=False,
        #     secure=settings.SECURE_COOKIES,
        #     samesite='Lax'
        # )

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            max_age=timedelta(days=7),
            httponly=True,
            secure=settings.SECURE_COOKIES,
            samesite="Lax",
        )

        return response


class LogoutUserView(APIView):
    """
    This view will handle logging out by clearing the refresh token cookie.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def post(self, request):
        """
        Log out the user by clearing the refresh token cookie.
        """
        response = Response({"message": "Logout successful."}, status=200)

        # Remove the refresh_token cookie by setting an expiration date in the past
        response.delete_cookie("refresh_token")

        return response


class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # Get refresh token from cookies
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return Response(
                {"detail": "Refresh token not found in cookies."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        request.data["refresh"] = refresh_token

        # Call the original `post` method to get the new access token
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200 and "access" in response.data:
            # Decode the access token to get user id
            access_token = response.data["access"]
            decoded_token = AccessToken(access_token)
            user_id = decoded_token.get("user_id")

            # Add user_id to the response
            response.data["user_id"] = user_id

        return response


class AllUsersView(APIView):
    """
    Views for all users.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    @extend_schema(
        summary="Retrieve a list of all users",
        description="This endpoint returns all users from the system.",
        responses={
            200: UserSerializer(many=True),
            401: {"type": "object", "properties": {"error": {"type": "string"}}},
        },
    )
    def get(self, request):
        """
        Custom get method for retrieving all users.
        """

        try:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(
                {"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED
            )


class UserViewSet(APIView):
    """
    Views for individual user.
    """

    serializer_class = UserSerializer

    @extend_schema(
        summary="Retrieve a single user by user id",
        description="This endpoint returns a single user from the system.",
        responses={
            200: UserSerializer(),
            401: {"type": "object", "properties": {"error": {"type": "string"}}},
            404: {
                "type": "object",
                "properties": {"error": {"type": "string"}},
            },
        },
    )
    def get(self, request, pk):
        """
        Custom get method for retrieving a single user.
        """
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = UserSerializer(user)
        return Response(serializer.data)

    @extend_schema(
        summary="Update a user by user id",
        description="This endpoint allows partial update for user details.",
        responses={
            200: UserSerializer(),
            400: {
                "type": "object",
                "properties": {"error": {"type": "string"}},
            },  # Handle 400 for invalid data
            401: {"type": "object", "properties": {"error": {"type": "string"}}},
            404: {
                "type": "object",
                "properties": {"error": {"type": "string"}},
            },  # Handle 404 for user not found
        },
    )
    def patch(self, request, pk):
        """
        Custom patch method for user.
        """
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        serializer = UserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            updated_user = serializer.save()
            response_serializer = UserSerializer(updated_user)
            return Response(response_serializer.data, status=200)

        return Response(serializer.errors, status=400)

    @extend_schema(
        summary="Delete a user by user id",
        description="This endpoint deletes a user from the system.",
        responses={
            204: {"description": "User deleted successfully"},
            404: {
                "type": "object",
                "properties": {"error": {"type": "string"}},
            },  # Handle 404 for user not found
        },
    )
    def delete(self, request, pk):
        """
        Custom delete method for user.
        """
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        user.delete()

        return Response(
            {"detail": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT
        )


class ChangePasswordView(APIView):
    """
    View to change a user's password.
    """

    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=ChangePasswordSerializer,
        responses={
            200: OpenApiResponse(description="Password changed successfully."),
            400: OpenApiResponse(
                description="Bad Request (old password is incorrect)."
            ),
        },
    )
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            old_password = serializer.validated_data["old_password"]
            new_password = serializer.validated_data["new_password"]

            if not request.user.check_password(old_password):
                return Response(
                    {"detail": "Old password is incorrect."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            request.user.set_password(new_password)
            request.user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
