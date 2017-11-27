from django.views import View

from app.response.services import ResponseService


class MailGroupInviteView(View):

    response_service = ResponseService()

    def get(self, request):
        return self.response_service.billshare_redirect()
