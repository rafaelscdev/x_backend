from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Post
from .serializers import PostSerializer

# Create your views here.

class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return get_object_or_404(Post, pk=self.kwargs['pk'])

    def perform_update(self, serializer):
        if serializer.instance.user != self.request.user:
            return Response(
                {"detail": "You don't have permission to edit this post."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            return Response(
                {"detail": "You don't have permission to delete this post."},
                status=status.HTTP_403_FORBIDDEN
            )
        instance.delete()

class PostLikeView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        post = self.get_object()
        user = request.user

        if post.likes.filter(id=user.id).exists():
            post.likes.remove(user)
            liked = False
        else:
            post.likes.add(user)
            liked = True

        serializer = self.get_serializer(post)
        return Response({
            'liked': liked,
            'likes_count': post.likes_count,
            **serializer.data
        })
