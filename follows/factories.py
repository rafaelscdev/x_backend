import factory

from follows.models import Follows
from users.factories import UsersFactory


class FollowsFactory(factory.django.DjangoModelFactory):
    follower = factory.SubFactory(UsersFactory)
    following = factory.SubFactory(UsersFactory)

    class Meta:
        model = Follows
