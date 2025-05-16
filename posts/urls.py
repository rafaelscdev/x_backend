from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .viewsets import PostViewSet, CommentViewSet

# Router principal para posts
router = DefaultRouter()
router.register(r'', PostViewSet, basename='posts')

# Router aninhado para comentários
posts_router = routers.NestedSimpleRouter(router, r'', lookup='post')
posts_router.register(r'comments', CommentViewSet, basename='post-comments')

urlpatterns = [
    path('following/', PostViewSet.as_view({'get': 'following'}), name='following-posts'),
    path('my_posts/', PostViewSet.as_view({'get': 'my_posts'}), name='my-posts'),
    path('liked/', PostViewSet.as_view({'get': 'liked'}), name='liked-posts'),
    path('', include(router.urls)),
    path('', include(posts_router.urls)),
] 