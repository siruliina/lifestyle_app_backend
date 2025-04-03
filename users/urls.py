from django.urls import path
from .views import (
    RegisterUserView,
    LoginUserView,
    LogoutUserView,
    CustomTokenRefreshView,
    UserViewSet,
    AllUsersView,
    ChangePasswordView,
)

urlpatterns = [
    # Token obtain view (Login)
    path("login/", LoginUserView.as_view(), name="login"),
    # Logout view = remove refresh token from cookies
    path("logout/", LogoutUserView.as_view(), name="logout"),
    # Registration view
    path("register/", RegisterUserView.as_view(), name="register"),
    # Token refresh view
    path("token/refresh/", CustomTokenRefreshView.as_view(), name="token-refresh"),
    # Basic user functions
    path("<int:pk>/", UserViewSet.as_view(), name="user-functions"),
    path(
        "change-password/",
        ChangePasswordView.as_view(),
        name="change-password",
    ),
    path("", AllUsersView.as_view(), name="all-users"),
]
