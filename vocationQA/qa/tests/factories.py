import factory

from django.conf import settings

from qa import models


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = settings.AUTH_USER_MODEL

    email = 'jhon@email.com'
    username = factory.Faker('user_name')
    password = 'secret'
    first_name = 'Jhon'
    last_name = 'Doe'

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default ``_create`` with our custom call."""
        manager = cls._get_manager(model_class)
        # The default would use ``manager.create(*args, **kwargs)``
        return manager.create_user(*args, **kwargs)


class DiscusionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Discusion

    cerrada = False


class PreguntaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Pregunta

    titulo = factory.Faker('sentence', nb_words=10)
    cuerpo = factory.Faker('text')
    autor = factory.SubFactory(UserFactory)


class RespuestaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Respuesta

    cuerpo = factory.Faker('text')
    autor = factory.SubFactory(UserFactory)
    discusion = factory.SubFactory(DiscusionFactory)


class FlagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Flag

    descripcion = factory.Faker('text')
    motivo = factory.Faker('sentence', nb_words=10)


class ObservationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Observacion

    usuario = factory.SubFactory(UserFactory)
    flag = factory.SubFactory(FlagFactory)
