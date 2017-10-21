from app.group.models import Group


class GroupService:
    def get(self, group_id):
        return Group.objects.get(pk=group_id)

    def create(self, label, user_id):
        return Group.objects.create(label=label, creator=user_id)

    def update(self, group_id, updated_fields):
        return Group.objects.filter(pk=group_id).update(updated_fields)

    def delete(self, group_id):
        return Group.objects.get(pk=group_id).delete()
