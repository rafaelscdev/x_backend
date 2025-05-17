from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .viewsets import FollowViewSet

router = DefaultRouter()
router.register(r"user", FollowViewSet, basename="follows")

urlpatterns = [
    path("", include(router.urls)),
]
