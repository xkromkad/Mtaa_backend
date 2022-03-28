from abc import ABC
from learning import models

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=models.Users.objects.all())

    class Meta:
        model = models.Users
        fields = ['id', 'name', 'surname', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True},
                        'name': {'write_only': True},
                        'surname': {'write_only': True}}
