from rest_framework import viewsets
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Entry
from .filters import EntryFilter
from .serializers import EntrySerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


class EntryViewSet(viewsets.ModelViewSet):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    )
    filterset_class = EntryFilter
    ordering_fields = ["created_at", "title"]
    ordering = ["created_at", "title"]
    search_fields = ["title"]

    @action(detail=True, methods=["post"])
    def toggle_favorite(self, request, pk=None):
        try:
            entry = self.get_object()
        except Entry.DoesNotExist:
            return Response(
                {"detail": "Entry not found."}, status=status.HTTP_404_NOT_FOUND
            )

        # Toggle the favorite value
        entry.favorite = not entry.favorite
        entry.save()

        # Return the updated entry
        serializer = EntrySerializer(entry)
        return Response(serializer.data, status=status.HTTP_200_OK)
