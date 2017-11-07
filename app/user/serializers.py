from rest_framework import serializers

from app.user.models import User


class AuthUserSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=255, allow_blank=False)
    password = serializers.CharField(required=True, max_length=128, allow_blank=False)


class UserIdSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = User
        fields = ['id']


class UserSerializer(serializers.ModelSerializer):
    last_login = serializers.DateTimeField(required=False)

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'first_name',
            'last_login',
            'last_name',
            'password',
        ]

    def to_representation(self, instance):
        data = super(UserSerializer, self).to_representation(instance)
        data.pop('password')
        return data
