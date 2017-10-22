from django.forms import model_to_dict
from django.core.exceptions import ObjectDoesNotExist

from app.group.models import Group, GroupUser
from app.user.models import User
from app.user.services import UserService


class GroupService:
    def get(self, group_id):
        group = Group.objects.get(pk=group_id)
        group_users = GroupUser.objects.filter(group=group)

        user_service = UserService()

        users = []
        for user in group_users:
            users.append(user_service.get(user.user_id))

        creator = user_service.get(group.creator.id)

        group_dict = model_to_dict(group)
        group_dict['users'] = users
        group_dict['creator'] = creator

        return group_dict

    def create(self, label, creator_email, memebers_emails):
        creator = User.objects.get(email=creator_email)
        group = Group.objects.create(label=label, creator=creator)

        for email in memebers_emails:
            try:
                user = User.objects.get(email=email)
                GroupUser.objects.create(group=group, user=user)
            except ObjectDoesNotExist:
                pass

        return self.get(group.id)

    def update(self, group_id, updated_fields):
        Group.objects.filter(pk=group_id).update(updated_fields)

    def delete(self, group_id):
        Group.objects.get(pk=group_id).delete()
