from django.urls import include, path
from rest_framework import routers

from follows.viewsets import FollowsViewSet

router = routers.SimpleRouter()
router.register(r"", FollowsViewSet, basename="follows")

urlpatterns = [
    path("", include(router.urls)),
]
