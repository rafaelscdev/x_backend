from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from .models import Post
from .serializers import PostSerializer

# Create your views here.

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class PostListCreateView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = Post.objects.all()
        # Filtro por usuário específico
        user_id = self.request.query_params.get('user_id', None)
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        return queryset

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
                {"detail": "Você não tem permissão para editar este post."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            return Response(
                {"detail": "Você não tem permissão para deletar este post."},
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
