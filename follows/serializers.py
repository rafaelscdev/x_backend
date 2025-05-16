from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Follow

User = get_user_model()

class FollowSerializer(serializers.ModelSerializer):
    follower_username = serializers.SerializerMethodField()
    following_username = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = ('id', 'follower', 'follower_username', 'following', 'following_username', 'created_at')
        read_only_fields = ('id', 'follower', 'created_at')

    def get_follower_username(self, obj):
        return obj.follower.username

    def get_following_username(self, obj):
        return obj.following.username

    def validate(self, data):
        if data['following'] == self.context['request'].user:
            raise serializers.ValidationError("Você não pode seguir a si mesmo.")
        return data

    def create(self, validated_data):
        validated_data['follower'] = self.context['request'].user
        return super().create(validated_data)

class UserFollowStatsSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'followers_count', 'following_count')

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count() 