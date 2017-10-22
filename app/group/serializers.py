from rest_framework import serializers


class GroupIdSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True, max_value=2147483647)


class GroupLabelSerializer(serializers.Serializer):
    label = serializers.CharField(required=True, max_length=255, min_length=1)
