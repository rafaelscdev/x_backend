from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .viewsets import RegisterViewSet, UserViewSet

router = DefaultRouter()
router.register(r"", UserViewSet, basename="users")

urlpatterns = [
    path("register/", RegisterViewSet.as_view(), name="register"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "me/",
        UserViewSet.as_view({"get": "me", "put": "me", "patch": "me"}),
        name="user-me",
    ),
    path("", include(router.urls)),
]
