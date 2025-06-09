from rest_framework import serializers

from follows.models import Follows
from posts.models import Comment, Post


class PostSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()
    follow_id = serializers.SerializerMethodField()
    profile_image = serializers.SerializerMethodField()  # Adicionado

    class Meta:
        model = Post
        fields = [
            "id",
            "user",
            "username",
            "content",
            "created_at",
            "likes_count",
            "is_liked",
            "comments_count",
            "is_following",
            "follow_id",
            "profile_image",  # Adicionado
        ]

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_is_liked(self, obj):
        user = self.context["request"].user
        return obj.likes.filter(id=user.id).exists() if user.is_authenticated else False

    def get_comments_count(self, obj):
        return obj.comments.count()

    def get_is_following(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return Follows.objects.filter(
                follower=request.user, following=obj.user
            ).exists()
        return False

    def get_follow_id(self, obj):
        user = self.context["request"].user
        if user.is_authenticated:
            follow = Follows.objects.filter(follower=user, following=obj.user).first()
            return follow.id if follow else None
        return None

    def get_profile_image(self, obj):
        if obj.user.profile_image:
            return obj.user.profile_image.url
        return None


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    username = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ["id", "content", "user", "created_at", "username"]

    def get_username(self, obj):
        return obj.user.username
