# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EntryViewSet

# Luo router
router = DefaultRouter()
router.register(r"", EntryViewSet, basename="entry")

# Rekisteröi router URL:iin
urlpatterns = [
    path("", include(router.urls)),
]
