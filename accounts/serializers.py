from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import PublisherProfile, AdvertiserProfile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


User = get_user_model()

class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'password', 'user_type')

class PublisherProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublisherProfile
        fields = ('phone',)  # Add other fields as needed

class AdvertiserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertiserProfile
        fields = ('phone',)  # Add other fields as needed

class CustomUserSerializer(UserCreateSerializer):
    publisher_profile = PublisherProfileSerializer(required=False)
    advertiser_profile = AdvertiserProfileSerializer(required=False)

    class Meta(UserCreateSerializer.Meta):
        fields = ('id', 'email', 'first_name', 'last_name', 'password', 'user_type', 'publisher_profile', 'advertiser_profile')

    def create(self, validated_data):
        user_type = validated_data.pop('user_type')
        publisher_profile = validated_data.pop('publisher_profile', None)
        advertiser_profile = validated_data.pop('advertiser_profile', None)

        user = User.objects.create_user(**validated_data, user_type=user_type)

        if user_type == 'student' and publisher_profile:
            PublisherProfile.objects.create(user=user, **publisher_profile)
        elif user_type == 'teacher' and advertiser_profile:
            AdvertiserProfile.objects.create(user=user, **advertiser_profile)

        return user
    


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['user_type'] = user.user_type  # Assuming user_type is a field in your User model
        # You can add other custom claims here

        return token