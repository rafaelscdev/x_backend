from django.test import TestCase

from posts.factories import PostFactory
from users.factories import UsersFactory


class TestPostModel(TestCase):
    def setUp(self):
        self.user = UsersFactory(username="joao")
        self.other_user = UsersFactory(username="maria")
        self.post = PostFactory(user=self.user, content="Primeiro post!")

    def test_post_creation(self):
        self.assertEqual(self.post.user, self.user)
        self.assertEqual(self.post.content, "Primeiro post!")
