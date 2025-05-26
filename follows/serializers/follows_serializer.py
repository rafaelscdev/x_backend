from django.contrib.auth import get_user_model
from rest_framework import serializers

from follows.models import Follows

User = get_user_model()


class UserBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username")


class FollowsSerializer(serializers.ModelSerializer):
    follower_username = serializers.CharField(
        source="follower.username", read_only=True
    )
    following_username = serializers.CharField(
        source="following.username", read_only=True
    )

    class Meta:
        model = Follows
        fields = [
            "id",
            "follower",
            "following",
            "follower_username",
            "following_username",
        ]
        extra_kwargs = {"follower": {"read_only": True}}

    def validate(self, data):
        request = self.context.get("request")
        if request and request.user == data["following"]:
            raise serializers.ValidationError({"non_field_errors": ["already exists"]})

        if Follows.objects.filter(
            follower=request.user, following=data["following"]
        ).exists():
            raise serializers.ValidationError({"non_field_errors": ["already exists"]})

        return data
