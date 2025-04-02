import django_filters
from .models import Entry


class EntryFilter(django_filters.FilterSet):
    # Filtering by only date and not the time
    created_at = django_filters.DateTimeFilter(
        field_name="created_at", lookup_expr="date"
    )

    class Meta:
        model = Entry
        fields = ["author", "created_at", "favorite"]
