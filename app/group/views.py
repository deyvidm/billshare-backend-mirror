import json

from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from app.group.serializers import GroupIdSerializer, GroupLabelSerializer
from app.group.services import GroupService
from app.response.services import ResponseService
from app.user.serializers import EmailSerializer


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

        # TODO not sure what this response should be.
        return self.response_service.success({})

    def post(self, request):
        try:
            body = json.loads(request.body)
        except Exception as e:
            return self.response_service.service_exception({'error': str(e)})

        valid_label = GroupLabelSerializer(data={
            'label': body.get('label', False)
        })
        if valid_label.is_valid() is False:
            return self.response_service.invalid_id({'error': valid_label.errors})

        valid_creator = EmailSerializer(data={
            'email': body.get('creator', False)
        })
        if valid_creator.is_valid() is False:
            return self.response_service.invalid_id({'error': valid_creator.errors})

        if body.get('members', False) is False:
            return self.response_service.invalid_id({'error': 'missing members'})

        for member in body.get('members'):
            valid_member = EmailSerializer(data={
                'email': member
            })
            if valid_member.is_valid() is False:
                return self.response_service.invalid_id({'error': valid_member.errors})

        group = self.group_service.create(
            label=body['label'],
            creator_email=body['creator'],
            memebers_emails=body['members']
        )

        return self.response_service.success({"request": group})
