from rest_framework import serializers


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=255, allow_blank=False)


class UserSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=255, allow_blank=False)
    first_name = serializers.CharField(required=True, max_length=255)
    last_name = serializers.CharField(required=True, max_length=255)


class UserIdSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True, max_value=2147483647)
