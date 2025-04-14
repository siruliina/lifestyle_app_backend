import django_filters
from .models import Checklist


class ChecklistFilter(django_filters.FilterSet):
    class Meta:
        model = Checklist
        fields = ["author"]
