from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, redirect

from .serializer import RegisterSerializer, ForgotPasswordSerializer, RestorePasswordSerializer
from .models import UserModel
from .send_email import send_reset_password


class RegisterUserView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Вы успешно зарегестрировались', status=201)


class ActivateView(APIView):
    def get(self, request):
        activation_code = request.query_params.get('u')
        user = get_object_or_404(UserModel, activation_code=activation_code)
        user.is_active = True
        user.activation_code = ''
        user.save()
        return redirect('https://google.com')


class ForgotPasswordView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = UserModel.objects.get(email=serializer.data.get('email'))
            user.create_activation_code()
            user.save()
            send_reset_password(user)
            return Response('Check your gmail')
        except UserModel.DoesNotExist:
            return Response('User with this email doees not exist')


class RestorePasswordView(APIView):
    def post(self, request):
        serializer = RestorePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Password changed successfully')
