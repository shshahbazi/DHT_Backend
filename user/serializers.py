import datetime
import random

from django.utils import timezone
from rest_framework import serializers, exceptions

from user.models import CustomUser


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def create(self, **kwargs):
        user, created = CustomUser.objects.get_or_create(email=self.validated_data.get('email'))

        if not created and timezone.now() < user.otp_expire:
            otp = user.otp
            otp_expire = user.otp_expire
        else:
            otp = random.randint(100000, 999999)
            otp_expire = timezone.now() + datetime.timedelta(minutes=10)

        user.otp = otp
        user.otp_expire = otp_expire

        return user


class AuthTokenSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    class Meta:
        model = CustomUser
        fields = ('email', 'otp')
        extra_kwargs = {'otp': {'write_only': True}}

    def validate(self, data):
        email = data.get('email')
        otp = data.get('otp')

        if not email or not otp:
            raise exceptions.ValidationError('Must include "email" and "otp".')

        user = CustomUser.objects.filter(email=email).first()
        if not user:
            raise exceptions.ValidationError('User not found')

        if timezone.now() > user.otp_expire:
            raise exceptions.ValidationError('OTP expired!')

        if otp != user.otp:
            raise exceptions.ValidationError('Wrong OTP')

        data['user'] = user
        return data


class OutputUserLoginSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'token']

    def get_token(self, obj):
        return self.context.get('token')


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
