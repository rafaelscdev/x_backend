from django.test import TestCase

from follows.factories import FollowsFactory
from follows.models import Follows


class TestFollowsModel(TestCase):
    def setUp(self):
        self.follow = FollowsFactory()

    def test_follow_created(self):
        self.assertEqual(Follows.objects.count(), 1)
        self.assertEqual(self.follow.follower.following.first(), self.follow)
        self.assertEqual(self.follow.following.followers.first(), self.follow)
        self.assertNotEqual(self.follow.follower, self.follow.following)

    def test_str_representation(self):
        expected = f"{self.follow.follower.username} → {self.follow.following.username}"
        self.assertEqual(str(self.follow), expected)
