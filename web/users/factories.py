import factory

from users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Faker('name')
    class Meta:
        model = User
