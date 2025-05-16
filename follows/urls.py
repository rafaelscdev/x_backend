from django.urls import path
from .views import (
    FollowUserView,
    UnfollowUserView,
    UserFollowStatsView,
    UserFollowersListView,
    UserFollowingListView
)

urlpatterns = [
    path('users/<int:user_id>/follow/', FollowUserView.as_view(), name='follow-user'),
    path('users/<int:user_id>/unfollow/', UnfollowUserView.as_view(), name='unfollow-user'),
    path('users/<int:user_id>/stats/', UserFollowStatsView.as_view(), name='user-follow-stats'),
    path('users/<int:user_id>/followers/', UserFollowersListView.as_view(), name='user-followers'),
    path('users/<int:user_id>/following/', UserFollowingListView.as_view(), name='user-following'),
] 