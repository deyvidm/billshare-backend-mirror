from django.http import JsonResponse
from django.conf import settings


class ResponseService():

    def success(self, response):
        return JsonResponse(
            data=response,
            status=200,
        )

    def invalid_id(self, response):
        return self.__prod_sanitization({
            'data': response,
            'status': 404,
        })

    def service_exception(self, response={}):
        return self.__prod_sanitization({
            'data': response,
            'status': 404,
        })

    def __prod_sanitization(self, params):
        if settings.DJANGO_ENV_IS_PROD:
            params['data'] = {}

        return JsonResponse(**params)
