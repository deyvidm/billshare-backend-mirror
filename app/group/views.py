import json

from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from app.group.serializers import GroupIdSerializer, CreateGroupSerializer
from app.group.services import GroupService
from app.response.services import ResponseService


@method_decorator(csrf_exempt, name='dispatch')
class GroupView(View):

    group_service = GroupService()
    response_service = ResponseService()

    def get(self, request, group_id=None):

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

    def delete(self, request, group_id=None):
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

    def post(self, request, group_id=None):
        try:
            request_data = json.loads(request.body)
        except ValueError as e:
            return self.response_service.json_decode_exception({'error': str(e)})

        valid_create_group = CreateGroupSerializer(data=request_data)
        if valid_create_group.is_valid() is False:
            return self.response_service.invalid_id({'error': valid_create_group.errors})

        group = self.group_service.create(
            label=request_data['label'],
            creator_email=request_data['creator'],
            user_emails=request_data['group_users']
        )

        if group is None:
            return self.response_service.service_exception({'error': 'There was an error'})

        return self.response_service.success(group)


class GroupTransactionsView(View):

    response_service = ResponseService()
    group_service = GroupService()

    def get(self, request, group_id):
        valid_group = GroupIdSerializer(data={'id': group_id})
        if valid_group.is_valid() is False:
            return self.response_service.invalid_id({'error': valid_group.errors})

        try:
            transactions = self.group_service.get_transactions(group_id)
        except Exception as e:
            return self.response_service.service_exception({'error': str(e)})

        return self.response_service.success(transactions)
