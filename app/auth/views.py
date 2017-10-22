import json

from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from app.user.serializers import AuthUserSerializer
from app.response.services import ResponseService
from app.auth.services import AuthService


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):

    auth_service = AuthService()
    response_service = ResponseService()

    def post(self, request):

        try:
            request_data = json.loads(request.body)
        except ValueError as e:
            return self.response_service.json_decode_exception({'error': str(e)})

        email = request_data.get('email', None)
        password = request_data.get('password', None)

        valid_credentials = AuthUserSerializer(data={
            'email': email,
            'password': password,
        })

        if valid_credentials.is_valid() is False:
            return self.response_service.invalid_id({'error': valid_credentials.errors})

        try:
            user = self.auth_service.authenticate(request=request, email=email, password=password)
        except Exception as e:
            return self.response_service.service_exception({'error': str(e)})

        if user is None:
            return self.response_service.failure({'error': 'Failed to authenticate.'})

        return self.response_service.success(user)
