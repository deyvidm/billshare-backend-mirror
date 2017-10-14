from django.http import JsonResponse


class UrlHandlers():

    def handler403(self, request):
        return JsonResponse({
            'status_code': 404,
        })

    def handler404(self, request):
        return JsonResponse({
            'status_code': 404,
        })

    def handler500(self, request):
        return JsonResponse({
            'status_code': 500,
        })
