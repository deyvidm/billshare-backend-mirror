from django.views import View
from django.http import JsonResponse


class Users(View):

    def get(self, request):
        data = {
            'success': True,
            'data': 'this is some test data'
        }

        return JsonResponse(data)
