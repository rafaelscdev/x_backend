import factory

from users.models import Users


class UsersFactory(factory.django.DjangoModelFactory):
    username = factory.Faker("user_name")
    password = factory.PostGenerationMethodCall("set_password", "123")

    class Meta:
        model = Users
