from django.urls import path
from .views import (
    RegisterUserView,
    LoginUserView,
    CustomTokenRefreshView,
    UserViewSet,
    AllUsersView,
)

urlpatterns = [
    # Token obtain view (Login)
    path("login/", LoginUserView.as_view(), name="login"),
    # Registration view
    path("register/", RegisterUserView.as_view(), name="register"),
    # Token refresh view
    path("token/refresh/", CustomTokenRefreshView.as_view(), name="token-refresh"),
    # Basic user functions
    path("<int:pk>/", UserViewSet.as_view(), name="user-functions"),
    path("", AllUsersView.as_view(), name="all-users"),
]
