from django.db import models
from django.db.models.base import ModelState
from rest_framework import serializers
from .models import User, User_Profile
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=126,min_length=6,write_only=True)

    class Meta:
        model = User
        fields = ['first_name','last_name','email','dob','address','company','password']

    def validate(self, attrs):
        email = attrs.get('email',None)
        first_name = attrs.get('first_name',None)
        last_name = attrs.get('last_name',None)
        dob = attrs.get('dob',None)
        address = attrs.get('address')
        company = attrs.get('company')

        if not first_name:
            raise serializers.ValidationError('First_name is required')

        if not email:
            raise serializers.ValidationError('Email id is required')

        if not last_name:
            raise serializers.ValidationError('Last_name is required')
        
        if not dob:
            raise serializers.ValidationError('Date of Birth is required')
        
        if not address:
            raise serializers.ValidationError('Address is required')
        
        if not company:
            raise serializers.ValidationError('Company is required')

        return attrs

    def create(self,validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=126,)
    password = serializers.CharField(max_length=126,min_length=6,write_only=True)
    access_token = serializers.CharField(max_length=264,read_only=True)
    refresh_token = serializers.CharField(max_length=264,read_only=True)
    is_auth = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = ['email','password','access_token','refresh_token','is_auth']

    def validate(self, attrs):
        email = attrs.get('email',None)
        password = attrs.get('password',None)
        
        user = authenticate(username=email,password=password)
        if not user:
            raise AuthenticationFailed("invalid credentials")
        if not user.is_active:
            raise AuthenticationFailed("user not activated")

        return {
            'email':user.email,
            'access_token':str(RefreshToken.for_user(user).access_token),
            'refresh_token':str(RefreshToken.for_user(user)),
            'is_auth':True
        }

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Profile