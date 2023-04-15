import factory
from django.contrib.auth.models import User
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task


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


class TaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Task
        django_get_or_create = ('name', 'description', 'status', 'created_by',
                                'assigned_to',)

    name = factory.Faker('sentence',
                         nb_words=2,
                         variable_nb_words=True,
                         )
    description = factory.Faker('text',
                                max_nb_chars=200,
                                )
    status = factory.SubFactory(StatusFactory)
    created_by = factory.SubFactory(UserFactory)
    assigned_to = factory.SubFactory(UserFactory)
