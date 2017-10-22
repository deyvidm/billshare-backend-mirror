import json

from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from app.group.serializers import GroupIdSerializer, GroupLabelSerializer, CreateGroupSerializer
from app.group.services import GroupService
from app.response.services import ResponseService


@method_decorator(csrf_exempt, name='dispatch')
class GroupView(View):

    group_service = GroupService()
    response_service = ResponseService()

    def get(self, request, group_id):

        valid_group = GroupIdSerializer(data={
            'id': group_id
        })

        if valid_group.is_valid() is False:
            return self.response_service.invalid_id({'error': valid_group.errors})

        try:
            group = self.group_service.get(group_id)
        except Exception as e:
            return self.response_service.service_exception({'error': str(e)})

        return self.response_service.success(group)

    def delete(self, request, group_id):
        valid_group = GroupIdSerializer(data={
            'id': group_id
        })

        if valid_group.is_valid() is False:
            return self.response_service.invalid_id({'error': valid_group.errors})

        try:
            self.group_service.delete(group_id)

        except Exception as e:
            return self.response_service.service_exception({'error': str(e)})

        return self.response_service.success({})

    def post(self, request):
        try:
            body = json.loads(request.body)
        except Exception as e:
            return self.response_service.service_exception({'error': str(e)})

        valid_create_group = CreateGroupSerializer(data={
            'label': body.get('label', False),
            'creator': body.get('creator', False),
            'group_users': body.get('group_users', False)
        })
        if valid_create_group.is_valid() is False:
            return self.response_service.invalid_id({'error': valid_create_group.errors})

        if body.get('group_users', False) is False:
            return self.response_service.invalid_id({'error': 'missing group users'})

        group = self.group_service.create(
            label=body['label'],
            creator_email=body['creator'],
            user_emails=body['group_users']
        )

        return self.response_service.success(group)
