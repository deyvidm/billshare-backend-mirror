from django.views import View
from app.group.serializers import GroupIdSerializer
from app.response.services import ResponseService
from app.group.services import GroupService, GroupUserService


class GroupView(View):
    def get(self, request, group_id):

        group_service = GroupService()
        group_user_service = GroupUserService()
        response_service = ResponseService()

        valid_group = GroupIdSerializer(data={
            'id': group_id
        })

        if valid_group.is_valid() is False:
            return response_service.invalid_id({'error': valid_group.errors})

        try:
            group = group_service.get(group_id)
            # group = group_user_service.get(group_id)

        except Exception as e:
            return response_service.service_exception({'error': str(e)})

        return response_service.success(group)

    def delete(self, request, group_id):

        response_service = ResponseService()
        return response_service.success(group_id)
