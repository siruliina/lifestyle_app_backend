# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChecklistViewSet

# Luo router
router = DefaultRouter()
router.register(r"", ChecklistViewSet, basename="checklist")

# Rekisteröi router URL:iin
urlpatterns = [
    path("", include(router.urls)),
]
