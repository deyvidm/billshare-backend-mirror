from app.group.models import Group, GroupUser
from app.user.models import User
from django.forms import model_to_dict


class GroupService:
    def get(self, group_id):
        group = Group.objects.get(pk=group_id)
        group_users = GroupUser.objects.filter(group=group)

        users = []
        for u in group_users:
            users.append(User.objects.get_user({'pk': u.user_id}))

        creator = User.objects.get_user({'pk': group.creator.id})
        return_dict = model_to_dict(group)
        return_dict['users'] = users
        return_dict['creator'] = creator

        return return_dict

    def create(self, label, user_id):
        Group.objects.create(label=label, creator=user_id)

    def update(self, group_id, updated_fields):
        Group.objects.filter(pk=group_id).update(updated_fields)

    def delete(self, group_id):
        Group.objects.get(pk=group_id).delete()


class GroupUserService:

    def add_users(self, group_id, user_ids):
        group = Group.objects.get(pk=group_id)
        for user_id in user_ids:
            user = User.objects.get(pk=user_id)
            GroupUser.objects.create(group=group, user=user)
