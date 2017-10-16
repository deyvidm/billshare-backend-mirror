from django.views import View
from django.http import JsonResponse


class UserView(View):

    def get(self, request):
        data = {
            'success': True,
        }

        return JsonResponse(data)
