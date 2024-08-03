from rest_framework import serializers, exceptions

from user.models import CustomUser


class AuthTokenSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})

    class Meta:
        model = CustomUser
        fields = ('email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        user = None
        if email and password:
            user = CustomUser.objects.filter(email=email).first()
            if not user:
                raise serializers.ValidationError("This email is not registered")
            if not user.check_password(password):
                raise serializers.ValidationError("Incorrect password")
        else:
            msg = 'Must include "email" and "password".'
            raise exceptions.ValidationError(msg)

        data['user'] = user
        return data


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = (
            'password',
            'first_name',
            'last_name',
            'email',)
        extra_kwargs = {'email': {'required': True}}

    def create(self, validated_data):
        user = CustomUser(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
