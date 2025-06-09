from rest_framework import serializers

from follows.models import Follows
from users.models import Users


class UsersSerializer(serializers.ModelSerializer):
    is_following = serializers.SerializerMethodField()
    follow_id = serializers.SerializerMethodField()

    class Meta:
        model = Users
        fields = [
            "id",
            "username",
            "email",
            "password",
            "profile_image",
            "is_following",
            "follow_id",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = Users(
            username=validated_data["username"], email=validated_data.get("email", "")
        )
        user.set_password(validated_data["password"])
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

    def get_is_following(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return Follows.objects.filter(follower=request.user, following=obj).exists()
        return False

    def get_follow_id(self, obj):
        user = self.context["request"].user
        if user.is_authenticated:
            follow = Follows.objects.filter(follower=user, following=obj).first()
            return follow.id if follow else None
        return None
