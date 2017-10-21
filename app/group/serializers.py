from rest_framework import serializers


class GroupIdSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True, max_value=2147483647)
