from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post

User = get_user_model()

class PostSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    likes_count = serializers.IntegerField(read_only=True)
    user_liked = serializers.SerializerMethodField()
    user_username = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'user', 'user_username', 'content', 'image', 'created_at', 'updated_at', 'likes_count', 'user_liked')
        read_only_fields = ('id', 'created_at', 'updated_at')

    def get_user_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(id=request.user.id).exists()
        return False

    def get_user_username(self, obj):
        return obj.user.username

    def validate_content(self, value):
        if len(value.strip()) == 0:
            raise serializers.ValidationError("O conteúdo não pode estar vazio.")
        if len(value) > 280:  # Limite do Twitter/X
            raise serializers.ValidationError("O conteúdo não pode ter mais de 280 caracteres.")
        return value

    def validate_image(self, value):
        if value:
            if value.size > 5 * 1024 * 1024:  # 5MB
                raise serializers.ValidationError("A imagem não pode ter mais de 5MB.")
            if not value.content_type.startswith('image/'):
                raise serializers.ValidationError("O arquivo deve ser uma imagem.")
        return value

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data) 