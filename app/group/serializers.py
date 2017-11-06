from rest_framework import serializers

from app.group.models import Group


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
