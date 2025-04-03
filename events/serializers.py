from rest_framework import serializers
from .models import Event


class EventSerializer(serializers.ModelSerializer):
    start_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    end_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Event
        fields = ["id", "title", "description", "start_date", "end_date", "author"]
