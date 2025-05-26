from django.urls import include, path
from rest_framework import routers

from users import viewsets

router = routers.SimpleRouter()
router.register(r"", viewsets.UsersViewSet, basename="users")

urlpatterns = [
    path("", include(router.urls)),
]
