import datetime
import random

from django.utils import timezone
from rest_framework import serializers, exceptions

from habit.models import WorkSession
from mental.models import DailyMood, DailyUserQuote
from mental.utils import get_new_quote
from scoring.serializers import UserScoreOutputSerializer
from user.models import CustomUser, Profile


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


class OutputProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    score = serializers.IntegerField(source='user.userscore.score', read_only=True)
    mood = serializers.SerializerMethodField()
    start_work_session = serializers.SerializerMethodField()
    daily_quote = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = '__all__'

    def get_mood(self, obj):
        user_mood = DailyMood.objects.filter(user=obj.user, created_at__day=timezone.now().day).first()

        if not user_mood:
            return None
        return user_mood.mood

    def get_start_work_session(self, obj):
        work_session = WorkSession.objects.filter(user=obj.user, end_time=None).first()

        if not work_session:
            return None
        return work_session.start_time

    def get_daily_quote(self, obj):
        if DailyUserQuote.objects.filter(user=obj.user, created_at__day=timezone.now().day).exists():
            return DailyUserQuote.objects.filter(user=obj.user, created_at__day=timezone.now().day).first().sentence

        sentence = get_new_quote(obj.user, self.get_mood(obj))
        DailyUserQuote.objects.create(sentence=sentence, user=obj.user)
        return sentence


class ProfileInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['picture']

    def validate_picture(self, value):
        if value is None:
            return value

        if not self.instance.allowed_change_profile:
            raise exceptions.ValidationError('You are not allowed to change your profile picture')

        return value

