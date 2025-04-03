# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet

# Luo router
router = DefaultRouter()
router.register(r"", EventViewSet, basename="event")

# Rekisteröi router URL:iin
urlpatterns = [
    path("", include(router.urls)),
]
