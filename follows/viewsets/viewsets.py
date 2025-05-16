from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from ..models import Follow
from ..serializers import FollowSerializer

User = get_user_model()

class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Follow.objects.select_related('follower', 'followed')

    def perform_create(self, serializer):
        followed = serializer.validated_data.get('followed')
        if followed == self.request.user:
            raise ValidationError({'error': 'Você não pode seguir a si mesmo.'})
        serializer.save(follower=self.request.user)

    @action(detail=True, methods=['post'])
    def follow_user(self, request, pk=None):
        user_to_follow = get_object_or_404(User, pk=pk)
        
        if request.user == user_to_follow:
            raise ValidationError({'error': 'Você não pode seguir a si mesmo.'})

        follow, created = Follow.objects.get_or_create(
            follower=request.user,
            followed=user_to_follow
        )

        if not created:
            return Response(
                {'error': 'Você já segue este usuário.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(follow)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['delete'])
    def unfollow_user(self, request, pk=None):
        user_to_unfollow = get_object_or_404(User, pk=pk)
        follow = get_object_or_404(
            Follow,
            follower=request.user,
            followed=user_to_unfollow
        )
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get'])
    def followers(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        follows = Follow.objects.filter(followed=user).select_related('follower')
        serializer = self.get_serializer(follows, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def following(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        follows = Follow.objects.filter(follower=user).select_related('followed')
        serializer = self.get_serializer(follows, many=True)
        return Response(serializer.data) 