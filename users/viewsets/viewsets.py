from rest_framework import viewsets, generics, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.db.models import Count
from ..serializers import UserSerializer, RegisterSerializer
from posts.models import Post

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create']:
            return [permissions.AllowAny()]
        elif self.action == 'me':
            return [permissions.IsAuthenticated()]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            UserSerializer(user).data,
            status=status.HTTP_201_CREATED
        )

    @action(detail=False, methods=['get', 'put', 'patch'])
    def me(self, request):
        if request.method == 'GET':
            return Response(self.get_serializer(request.user).data)
        
        serializer = self.get_serializer(
            request.user,
            data=request.data,
            partial=request.method == 'PATCH'
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        """Retorna estatísticas do usuário"""
        user = self.get_object()
        
        # Contagem de seguidores e seguindo
        followers_count = user.followers.count()
        following_count = user.following.count()
        
        # Contagem de posts
        posts_count = Post.objects.filter(user=user).count()
        
        # Contagem de likes recebidos
        likes_received = Post.objects.filter(user=user).aggregate(
            total_likes=Count('likes')
        )['total_likes'] or 0
        
        # Contagem de likes dados
        likes_given = user.liked_posts.count()
        
        return Response({
            'followers_count': followers_count,
            'following_count': following_count,
            'posts_count': posts_count,
            'likes_received': likes_received,
            'likes_given': likes_given
        })

class RegisterViewSet(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            UserSerializer(user).data,
            status=status.HTTP_201_CREATED
        ) 