from rest_framework import viewsets

from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Checklist

from .serializers import ChecklistSerializer
from .filters import ChecklistFilter


class ChecklistViewSet(viewsets.ModelViewSet):
    queryset = Checklist.objects.all()
    serializer_class = ChecklistSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ChecklistFilter
