import pytest
from rest_framework.test import APIClient

from follows.factories import FollowsFactory
from follows.models import Follows
from users.factories import UsersFactory


@pytest.mark.django_db
class TestFollowsViewSet:

    def setup_method(self):
        self.client = APIClient()
        self.user1 = UsersFactory()
        self.user2 = UsersFactory()
        self.client.force_authenticate(user=self.user1)

    def test_follow_user(self):
        response = self.client.post("/api/follows/", data={"following": self.user2.id})
        assert response.status_code == 201
        assert Follows.objects.filter(
            follower=self.user1, following=self.user2
        ).exists()

    def test_unfollow_user(self):
        follow = FollowsFactory(follower=self.user1, following=self.user2)
        response = self.client.delete(f"/api/follows/{follow.id}/")
        assert response.status_code == 204
        assert not Follows.objects.filter(id=follow.id).exists()

    def test_follow_duplicate(self):
        FollowsFactory(follower=self.user1, following=self.user2)
        response = self.client.post("/api/follows/", data={"following": self.user2.id})
        assert response.status_code == 400
        assert "already exists" in response.data["non_field_errors"][0].lower()
