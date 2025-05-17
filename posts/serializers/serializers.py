from rest_framework import serializers

from ..models import Comment, Post


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "post", "user", "username", "content", "created_at")
        read_only_fields = ("id", "user", "post", "created_at")

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class PostSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "user",
            "username",
            "content",
            "created_at",
            "updated_at",
            "likes_count",
            "comments_count",
            "comments",
        )
        read_only_fields = ("id", "user", "created_at", "updated_at")

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comments_count(self, obj):
        return obj.comments.count()

    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("O conteúdo não pode estar vazio.")
        if len(value) > 280:
            raise serializers.ValidationError(
                "O conteúdo não pode ter mais de 280 caracteres."
            )
        return value

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
