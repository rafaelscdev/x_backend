from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import FollowViewSet

router = DefaultRouter()
router.register(r'', FollowViewSet, basename='follows')

urlpatterns = [
    path('', include(router.urls)),
    path('user/<int:pk>/follow/', FollowViewSet.as_view({'post': 'follow_user', 'delete': 'unfollow_user'}), name='follow-user'),
    path('user/<int:pk>/followers/', FollowViewSet.as_view({'get': 'followers'}), name='user-followers'),
    path('user/<int:pk>/following/', FollowViewSet.as_view({'get': 'following'}), name='user-following'),
] 