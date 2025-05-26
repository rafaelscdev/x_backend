from rest_framework import permissions, serializers, viewsets

from follows.models import Follows
from follows.serializers import FollowsSerializer


class FollowsViewSet(viewsets.ModelViewSet):
    serializer_class = FollowsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Follows.objects.filter(follower=self.request.user)

    def perform_create(self, serializer):
        if serializer.validated_data["following"] == self.request.user:
            raise serializers.ValidationError()
        serializer.save(follower=self.request.user)
