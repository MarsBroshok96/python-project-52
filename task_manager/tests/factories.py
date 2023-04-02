import factory
from django.contrib.auth.models import User
from task_manager.statuses.models import Status


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('first_name', 'last_name', 'username',
                                'password', 'email',)

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    username = factory.Faker('user_name')
    password = factory.Faker('password')
    email = factory.Faker('email')


class StatusFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Status
        django_get_or_create = ('name',)

    name = factory.Faker('sentence',
                         nb_words=2,
                         variable_nb_words=True,
                         )
