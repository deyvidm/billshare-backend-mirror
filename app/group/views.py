from django.views import View
from app.group.serializers import GroupIdSerializer
from app.response.services import ResponseService
from app.group.services import GroupService, GroupUserService
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name='dispatch')
class GroupView(View):

    group_service = GroupService()
    group_user_service = GroupUserService()
    response_service = ResponseService()

    def get(self, request, group_id):

        valid_group = GroupIdSerializer(data={
            'id': group_id
        })

        if valid_group.is_valid() is False:
            return self.response_service.invalid_id({'error': valid_group.errors})

        try:
            group = self.group_service.get(group_id)
            # group = group_user_service.get(group_id)

        except Exception as e:
            return self.response_service.service_exception({'error': str(e)})

        return self.response_service.success(group)

    def delete(self, request, group_id):
        return {":)": ":)"}
