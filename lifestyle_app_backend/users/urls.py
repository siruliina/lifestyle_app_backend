from django.urls import path
from .views import RegisterUserView, LoginUserView, CustomTokenRefreshView

urlpatterns = [
    # Token obtain view (Login)
    path('login/', LoginUserView.as_view(), name='login'),

    # Registration view
    path('register/', RegisterUserView.as_view(), name='register'),

    # Token refresh view
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),

    
]