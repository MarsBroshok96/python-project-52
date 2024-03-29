"""Factories for creating test data."""
import factory
from django.contrib.auth import get_user_model
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.labels.models import Label


User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    """A factory for creating users."""
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
    """A factory for creating statuses."""
    class Meta:
        model = Status
        django_get_or_create = ('name',)

    name = factory.Faker('sentence',
                         nb_words=2,
                         variable_nb_words=True,
                         )


class LabelFactory(factory.django.DjangoModelFactory):
    """A factory for creating labels."""
    class Meta:
        model = Label
        django_get_or_create = ('name',)

    name = factory.Faker('word')


class TaskFactory(factory.django.DjangoModelFactory):
    """A factory for creating tasks."""
    class Meta:
        model = Task

    name = factory.Faker('sentence',
                         nb_words=2,
                         variable_nb_words=True,
                         )
    description = factory.Faker('text',
                                max_nb_chars=200,
                                )
    status = factory.SubFactory(StatusFactory)
    created_by = factory.SubFactory(UserFactory)
    executor = factory.SubFactory(UserFactory)

    @factory.post_generation
    def labels(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for label in extracted:
                self.labels.add(label)
