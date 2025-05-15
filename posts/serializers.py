from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post

User = get_user_model()

class PostSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    likes_count = serializers.IntegerField(read_only=True)
    user_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'user', 'content', 'image', 'created_at', 'updated_at', 'likes_count', 'user_liked')
        read_only_fields = ('id', 'created_at', 'updated_at')

    def get_user_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(id=request.user.id).exists()
        return False

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data) 