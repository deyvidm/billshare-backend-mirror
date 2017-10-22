from rest_framework import serializers


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=255, allow_blank=False)


class GroupIdSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True, max_value=2147483647)


class GroupLabelSerializer(serializers.Serializer):
    label = serializers.CharField(required=True, max_length=255, min_length=1)


class CreateGroupSerializer(serializers.Serializer):
    label = serializers.CharField(required=True, max_length=255, min_length=1)
    creator = serializers.EmailField(required=True, max_length=255, allow_blank=False)
    group_users = serializers.ListField(
        child=serializers.EmailField(required=True, max_length=255, allow_blank=False)
    )
