from rest_framework import serializers

from app.user.models import User


class AuthUserSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=255, allow_blank=False)
    password = serializers.CharField(required=True, max_length=128, allow_blank=False)


class UserSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=255, allow_blank=False)
    first_name = serializers.CharField(required=True, max_length=255)
    last_name = serializers.CharField(required=True, max_length=255)


class UserIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user']

    user = serializers.IntegerField(required=True, source='id')
