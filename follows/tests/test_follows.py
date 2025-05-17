from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from follows.models import Follow

User = get_user_model()


class FollowTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="follower", email="follower@example.com", password="testpass123"
        )
        self.user2 = User.objects.create_user(
            username="followed", email="followed@example.com", password="testpass123"
        )
        self.follow = Follow.objects.create(follower=self.user1, followed=self.user2)

    def test_create_follow(self):
        """Teste de criação de relacionamento de follow"""
        self.assertEqual(self.follow.follower, self.user1)
        self.assertEqual(self.follow.followed, self.user2)
        self.assertTrue(
            Follow.objects.filter(follower=self.user1, followed=self.user2).exists()
        )

    def test_cannot_follow_self(self):
        """Teste que usuário não pode seguir a si mesmo"""
        with self.assertRaises(Exception):
            Follow.objects.create(follower=self.user1, followed=self.user1)


class FollowAPITests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="follower", email="follower@example.com", password="testpass123"
        )
        self.user2 = User.objects.create_user(
            username="followed", email="followed@example.com", password="testpass123"
        )
        self.client.force_authenticate(user=self.user1)

    def test_follow_user_api(self):
        """Teste de follow de usuário via API"""
        response = self.client.post(f"/api/follows/user/{self.user2.id}/follow_user/")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["follower"]["id"], self.user1.id)
        self.assertEqual(response.data["follower"]["username"], self.user1.username)
        self.assertEqual(response.data["followed"]["id"], self.user2.id)
        self.assertEqual(response.data["followed"]["username"], self.user2.username)

    def test_unfollow_user_api(self):
        """Teste de unfollow de usuário"""
        self.client.post(f"/api/follows/user/{self.user2.id}/follow_user/")
        response = self.client.delete(
            f"/api/follows/user/{self.user2.id}/unfollow_user/"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_list_followers(self):
        """Teste de listagem de seguidores"""
        Follow.objects.create(follower=self.user1, followed=self.user2)
        response = self.client.get(f"/api/follows/user/{self.user2.id}/followers/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["follower"]["username"], self.user1.username)

    def test_list_following(self):
        """Teste de listagem de usuários que segue"""
        Follow.objects.create(follower=self.user1, followed=self.user2)
        response = self.client.get(f"/api/follows/user/{self.user1.id}/following/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["followed"]["username"], self.user2.username)
