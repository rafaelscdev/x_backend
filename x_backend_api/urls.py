from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/users/", include("users.urls")),
    path("api/posts/", include("posts.urls")),
    path("api/follows/", include("follows.urls")),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
