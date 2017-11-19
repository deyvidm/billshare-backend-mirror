from rest_framework import serializers

from app.group.models import Group, GroupUser

from app.user.serializers import UserSerializer


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=255, allow_blank=False)


class GroupIdSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all())

    class Meta:
        model = Group
        fields = ['id']


class GroupLabelSerializer(serializers.Serializer):
    label = serializers.CharField(required=True, max_length=255, min_length=1)


class CreateGroupSerializer(serializers.Serializer):
    label = serializers.CharField(required=True, max_length=255, min_length=1)
    creator = serializers.EmailField(required=True, max_length=255, allow_blank=False)
    group_users = serializers.ListField(
        child=serializers.EmailField(required=True, max_length=255, allow_blank=False)
    )


class GroupSerializer(serializers.ModelSerializer):
    creator = UserSerializer(allow_null=False, required=True, many=False)
    group_users = UserSerializer(allow_null=False, required=True, many=True)

    class Meta:
        model = Group
        fields = [
            'id',
            'creator',
            'label',
            'group_users',
        ]

    def to_representation(self, instance):
        data = super(GroupSerializer, self).to_representation(instance)
        data.pop('creator')
        return data
