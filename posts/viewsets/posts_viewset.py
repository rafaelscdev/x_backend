from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination  # <-- Importação adicionada
from rest_framework.response import Response

from follows.models import Follows
from posts.models import Comment, Post
from posts.serializers import CommentSerializer, PostSerializer


# Classe de paginação personalizada
class PostPagination(PageNumberPagination):
    page_size = 10  # Você pode ajustar esse valor conforme desejar


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by("-created_at")
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = PostPagination  # <-- Paginação ativada

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(
        detail=False, methods=["get"], permission_classes=[permissions.IsAuthenticated]
    )
    def following(self, request):
        following_ids = Follows.objects.filter(follower=request.user).values_list(
            "following_id", flat=True
        )
        posts = Post.objects.filter(user_id__in=following_ids).order_by("-created_at")
        page = self.paginate_queryset(posts)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)

    @action(
        detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated]
    )
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        if post.likes.filter(id=user.id).exists():
            post.likes.remove(user)
            return Response({"status": "unliked"})
        else:
            post.likes.add(user)
            return Response({"status": "liked"})


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post_id = self.kwargs["post_id"]
        return Comment.objects.filter(post_id=post_id).order_by("-created_at")

    def perform_create(self, serializer):
        post_id = self.kwargs.get("post_id")
        post = get_object_or_404(Post, id=post_id)
        serializer.save(user=self.request.user, post=post)
