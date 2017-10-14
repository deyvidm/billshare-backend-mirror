from django.http import JsonResponse


def handler403(request):
    return JsonResponse(
        {},
        status=404,
    )


def handler404(request):
    return JsonResponse(
        {},
        status=404,
    )


def handler500(request):
    return JsonResponse(
        {},
        status=500,
    )
