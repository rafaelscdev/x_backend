from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .models import Follow
from .serializers import FollowSerializer, UserFollowStatsSerializer

User = get_user_model()

class FollowUserView(generics.CreateAPIView):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        following_user = get_object_or_404(User, pk=kwargs['user_id'])
        
        if Follow.objects.filter(follower=request.user, following=following_user).exists():
            return Response(
                {"detail": "Você já segue este usuário."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(data={'following': following_user.id})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UnfollowUserView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        following_user = get_object_or_404(User, pk=kwargs['user_id'])
        follow = get_object_or_404(
            Follow,
            follower=request.user,
            following=following_user
        )
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserFollowStatsView(generics.RetrieveAPIView):
    serializer_class = UserFollowStatsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return get_object_or_404(User, pk=self.kwargs['user_id'])

class UserFollowersListView(generics.ListAPIView):
    serializer_class = UserFollowStatsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.kwargs['user_id'])
        return user.followers.all()

class UserFollowingListView(generics.ListAPIView):
    serializer_class = UserFollowStatsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.kwargs['user_id'])
        return user.following.all()
