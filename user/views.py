from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, generics
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import CustomUser, Profile
from user.serializers import AuthTokenSerializer, OutputUserLoginSerializer, LoginSerializer, OutputProfileSerializer
from user.utils import send_otp


class AuthLoginUser(APIView):
    permission_classes = [AllowAny, ]

    @swagger_auto_schema(request_body=LoginSerializer(), responses={200: None}, tags=['Auth'])
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.create()
        user.save()
        send_otp(email=user.email, otp=user.otp)

        return Response(status=status.HTTP_200_OK)


class VerifyOTPLogin(ObtainAuthToken):
    permission_classes = [AllowAny, ]

    @swagger_auto_schema(
        request_body=AuthTokenSerializer(), responses={200: OutputUserLoginSerializer()}, tags=['Auth']
    )
    def post(self, request, *args, **kwargs):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        output_serializer = OutputUserLoginSerializer(instance=user, context={'token': token.key})
        return Response(output_serializer.data, status=status.HTTP_200_OK)


class LogOutApi(APIView):
    permission_classes = [IsAuthenticated, ]

    @swagger_auto_schema(responses={200: None}, tags=['Auth'])
    def get(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class GetProfileDetails(APIView):
    permission_classes = [IsAuthenticated, ]

    @swagger_auto_schema(responses={200: OutputProfileSerializer()}, tags=['Profile'])
    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        serializer = OutputProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
