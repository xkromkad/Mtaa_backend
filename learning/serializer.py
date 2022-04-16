
from learning import models

from django.contrib.auth.models import User
from rest_framework import serializers, validators

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Users
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True},
                        'name': {'write_only': True},
                        'surname': {'write_only': True}}


class FeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Feed
        fields = '__all__'

class Serializer_For_Register(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "password", "email", "first_name", "last_name")
        extra_kwargs = {
            "password": {"write_only": True},
            "email": dict(required=True, allow_blank=False),
            "first_name": dict(allow_blank=False),
            "last_name": dict(allow_blank=False),
            "username": dict(allow_blank=False),
        }

    def create(self, validated_data):
        serialized_obj = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"]
        )
        return serialized_obj