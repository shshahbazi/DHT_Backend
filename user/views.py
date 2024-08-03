from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, generics
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from user.models import CustomUser
from user.serializers import AuthTokenSerializer, OutputUserLoginSerializer, UserRegisterSerializer


class AuthLoginUser(ObtainAuthToken):
    permission_classes = [AllowAny,]

    @swagger_auto_schema(request_body=AuthTokenSerializer, responses={200: OutputUserLoginSerializer()})
    def post(self, request, *args, **kwargs):
        serializer = AuthTokenSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        output_serializer = OutputUserLoginSerializer(instance=user, context={'token': token.key})
        return Response(output_serializer.data, status=status.HTTP_200_OK)


class UserRegistrationView(generics.CreateAPIView):
    permission_classes = [AllowAny,]
    authentication_classes = []
    serializer_class = UserRegisterSerializer

    @swagger_auto_schema(request_body=UserRegisterSerializer, responses={201: UserRegisterSerializer()})
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        user_created = CustomUser.objects.get(email=serializer.data['email'])

        # TODO: send activation link

        return Response(serializer.data, status=status.HTTP_201_CREATED)
