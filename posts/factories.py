import factory

from posts.models import Post
from users.factories import UsersFactory


class PostFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UsersFactory)
    content = factory.Faker("sentence")

    class Meta:
        model = Post
