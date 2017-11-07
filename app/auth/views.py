import json

from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from app.user.serializers import AuthUserSerializer, UserSerializer
from app.user.services import UserService
from app.response.services import ResponseService
from app.auth.services import AuthService


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):

    def post(self, request):

        auth_service = AuthService()
        response_service = ResponseService()

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
            return response_service.invalid_id({'error': valid_credentials.errors})

        try:
            user = auth_service.authenticate(request=request, email=email, password=password)
        except Exception as e:
            return response_service.service_exception({'error': str(e)})

        if user is None:
            return response_service.failure({'error': 'Failed to authenticate.'})

        return response_service.success(user)


@method_decorator(csrf_exempt, name='dispatch')
class LogoutView(View):

    def post(self, request):

        auth_service = AuthService()
        response_service = ResponseService()

        auth_service.unauthenticate(request=request)

        return response_service.success({})


@method_decorator(csrf_exempt, name='dispatch')
class CreateUserView(View):

    def post(self, request):
        auth_service = AuthService()
        response_service = ResponseService()
        user_service = UserService()

        try:
            request_data = json.loads(request.body)
        except ValueError as e:
            return response_service.json_decode_exception({'error': str(e)})

        valid_user = UserSerializer(data=request_data)

        if valid_user.is_valid() is False:
            return response_service.invalid_id({'error': valid_user.errors})

        if user_service.email_exists(email=request_data['email']):
            return response_service.failure({'error': 'Email already exists'})

        try:
            user = auth_service.create_user(
                email=request_data['email'],
                password=request_data['password'],
                first_name=request_data['first_name'],
                last_name=request_data['last_name'],
            )
        except Exception as e:
            return response_service.service_exception({'error': str(e)})

        if user is None:
            return response_service.failure({'error': 'Failed to authenticate.'})

        # Login user before returning
        return LoginView.as_view()(self.request)
