import pytest
from rest_framework.test import APIClient

from follows.factories import FollowsFactory
from posts.factories import PostFactory
from posts.models import Post
from users.factories import UsersFactory


@pytest.mark.django_db
class TestPostViewSet:

    def setup_method(self):
        self.client = APIClient()
        self.user = UsersFactory()
        self.client.force_authenticate(user=self.user)

    def test_create_post(self):
        payload = {"content": "Meu primeiro post!"}
        response = self.client.post("/api/posts/", payload)
        assert response.status_code == 201
        assert Post.objects.filter(user=self.user).count() == 1

    def test_list_posts(self):
        PostFactory.create_batch(3)
        response = self.client.get("/api/posts/")
        assert response.status_code == 200
        assert len(response.data) == 3

    def test_detail_post(self):
        post = PostFactory()
        response = self.client.get(f"/api/posts/{post.id}/")
        assert response.status_code == 200
        assert response.data["id"] == post.id

    def test_following_posts(self):
        followed_user = UsersFactory()
        FollowsFactory(follower=self.user, following=followed_user)
        PostFactory(user=followed_user)
        PostFactory(user=self.user)

        response = self.client.get("/api/posts/following/")
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]["user"] == followed_user.id

    def test_like_post(self):
        post = PostFactory()
        response = self.client.post(f"/api/posts/{post.id}/like/")
        assert response.status_code == 200
        assert response.data["status"] == "liked"

        response = self.client.post(f"/api/posts/{post.id}/like/")
        assert response.status_code == 200
        assert response.data["status"] == "unliked"

    def test_create_comment(self):
        post = PostFactory()
        payload = {
            "content": "Comentando aqui!",
            "post": post.id,
        }
        response = self.client.post(f"/api/posts/{post.id}/comments/", payload)
        assert response.status_code == 201
