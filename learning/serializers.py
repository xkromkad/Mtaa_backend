from abc import ABC
from learning import models

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class meta:
        models = models.Users
        Fields = '__all__'
        extra_kwargs = {'password': {'write_only': True},
                        'name': {'write_only': True},
                        'surname': {'write_only': True}}


