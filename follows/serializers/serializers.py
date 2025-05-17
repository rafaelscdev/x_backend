from django.contrib.auth import get_user_model
from rest_framework import serializers

from ..models import Follow

User = get_user_model()


class UserBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username")


class FollowSerializer(serializers.ModelSerializer):
    follower = UserBasicSerializer(read_only=True)
    followed = UserBasicSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = ("id", "follower", "followed", "created_at")
        read_only_fields = ("id", "follower", "created_at")
