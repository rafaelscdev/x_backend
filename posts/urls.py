from django.urls import include, path
from rest_framework import routers

from posts.viewsets import CommentViewSet, PostViewSet

router = routers.SimpleRouter()
router.register(r"", PostViewSet, basename="posts")

posts_with_comments = [
    path(
        "<int:post_id>/comments/",
        CommentViewSet.as_view({"get": "list", "post": "create"}),
        name="post-comments-list",
    ),
    path(
        "<int:post_id>/comments/<int:pk>/",
        CommentViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
        name="post-comments-detail",
    ),
]

urlpatterns = [
    path("", include(router.urls)),
    path("", include(posts_with_comments)),
]
