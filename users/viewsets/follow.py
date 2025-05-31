from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models import Follow
from ..serializers import FollowSerializer


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Follow.objects.filter(follower=self.request.user)

    def perform_create(self, serializer):
        serializer.save(follower=self.request.user)

    @action(detail=True, methods=["post"])
    def follow(self, request, pk=None):
        user = self.get_object()
        if user == request.user:
            return Response(
                {"error": "Você não pode seguir a si mesmo"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        follow, created = Follow.objects.get_or_create(
            follower=request.user, following=user
        )

        if not created:
            return Response(
                {"error": "Você já segue este usuário"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(FollowSerializer(follow).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["delete"])
    def unfollow(self, request, pk=None):
        user = self.get_object()
        try:
            follow = Follow.objects.get(follower=request.user, following=user)
            follow.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Follow.DoesNotExist:
            return Response(
                {"error": "Você não segue este usuário"},
                status=status.HTTP_400_BAD_REQUEST,
            )
