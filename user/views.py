from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, generics
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import CustomUser
from user.serializers import AuthTokenSerializer, OutputUserLoginSerializer, LoginSerializer
from user.utils import send_otp


class AuthLoginUser(APIView):
    permission_classes = [AllowAny, ]

    @swagger_auto_schema(request_body=LoginSerializer(), responses={200: None})
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.create()
        user.save()
        send_otp(email=user.email, otp=user.otp)

        return Response(status=status.HTTP_200_OK)


class VerifyOTPLogin(ObtainAuthToken):
    permission_classes = [AllowAny, ]

    @swagger_auto_schema(request_body=AuthTokenSerializer(), responses={200: OutputUserLoginSerializer()})
    def post(self, request, *args, **kwargs):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        output_serializer = OutputUserLoginSerializer(instance=user, context={'token': token.key})
        return Response(output_serializer.data, status=status.HTTP_200_OK)


class LogOutApi(APIView):
    permission_classes = [IsAuthenticated, ]

    @swagger_auto_schema(responses={200: None})
    def get(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
