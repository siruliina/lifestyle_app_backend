from django.urls import path
from .views import RegisterUserView, CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # Token obtain view (Login)
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # Token refresh view
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Registration view
    path('register/', RegisterUserView.as_view(), name='register'),
]