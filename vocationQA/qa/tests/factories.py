from qa import models
from django.conf import settings
import factory



class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = settings.AUTH_USER_MODEL

    email = 'jhon@email.com'
    username = 'jhon'
    password = 'secret'
    first_name = 'Jhon'
    last_name = 'Doe'

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default ``_create`` with our custom call."""
        manager = cls._get_manager(model_class)
        # The default would use ``manager.create(*args, **kwargs)``
        return manager.create_user(*args, **kwargs)


class QuestionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Question

    title = 'My first question'
    body = 'bla bla bla bla'
    user = factory.SubFactory(UserFactory)