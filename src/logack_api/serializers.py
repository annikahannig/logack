
from rest_framework import serializers


class SubSerializer(serializers.ModelSerializer):
    """Sub serializer"""
    class Meta:
        model = Sub
        fields = ["id", "user_id", "name"]


class EventSerializer(serializers.ModelSerializer)
    """Event serializer"""
    class Meta:
        model = Event
        fields = ["id", "user_id", "sub_id", "label",
        "description", "ack"]

