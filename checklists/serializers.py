from rest_framework import serializers
from .models import Checklist, ChecklistItem


class ChecklistItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChecklistItem
        fields = ["id", "title", "finished"]


class ChecklistSerializer(serializers.ModelSerializer):
    checklist_items = ChecklistItemSerializer(many=True, required=False)

    def create(self, validated_data):
        checklist_items_data = validated_data.pop("checklist_items", [])

        checklist = Checklist.objects.create(**validated_data)

        for item_data in checklist_items_data:
            ChecklistItem.objects.create(checklist=checklist, **item_data)

        return checklist

    class Meta:
        model = Checklist
        fields = ["id", "title", "description", "author", "checklist_items"]
