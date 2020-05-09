import uuid as uuid_lib
from django.db.models import Count
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.urls.base import reverse
from django.utils.text import slugify
from model_utils.models import TimeStampedModel

# Create your models here.
class ContarVotos(models.Model):
    votos_positivos = models.PositiveIntegerField(default=0)
    votos_negativos = models.PositiveIntegerField(default=0)

    class Meta:
        abstract = True


class Etiqueta(models.Model):
    nombre = models.CharField(max_length=150)


class Flag(models.Model):
    motivo = models.CharField(max_length=150)
    descripcion = models.TextField()

    def __str__(self):
        return self.motivo


class Discusion(TimeStampedModel):
    cerrada = models.BooleanField(default=False)

    class Meta:
        ordering = ['-pregunta__created']


class Publicacion(TimeStampedModel, ContarVotos):
    TIPO_PUBLICACION = (
        (0, 'comentario'),
        (1, 'pregunta'),
        (2, 'respuesta'),
    )
    tipo = models.IntegerField(null=True, choices=TIPO_PUBLICACION)
    slug = models.SlugField(editable=False, max_length=255)
    cuerpo = models.TextField()
    autor = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    observaciones = models.ManyToManyField(
        Flag,
        through='Observacion',
        through_fields=('publicacion', 'flag')
    )


class Pregunta(Publicacion):
    titulo = models.CharField(max_length=150)
    discusion = models.OneToOneField(
        Discusion, on_delete=models.CASCADE)
    etiquetas = models.ManyToManyField(Etiqueta, blank=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.titulo

    def save(self, *args, **kwargs):
        '''
        Save redefinition to set slug and discusion fields
        '''
        self.tipo = 1
        self.slug = slugify(self.titulo)
        # Set discusion to new question
        if not self.pk:
            self.discusion = Discusion.objects.create()

        super().save(*args, **kwargs)

    def user_can_accept_answer(self, user):
        return self.autor == user


class Respuesta(Publicacion):
    discusion = models.ForeignKey(
        to=Discusion, on_delete=models.CASCADE, related_name='respuestas')
    aceptada = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created']

    def save(self, *args, **kwargs):
        self.tipo = 2
        self.slug = slugify(self.cuerpo[:50])
        super().save(*args, **kwargs)


class Comentario(Publicacion):
    publicacion = models.ForeignKey(
       to=Publicacion,
       on_delete=models.CASCADE,
       related_name='comentarios'
    )


class Observacion(TimeStampedModel):
    usuario = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    publicacion = models.ForeignKey(
        to=Publicacion, on_delete=models.PROTECT)
    flag = models.ForeignKey(
        to=Flag, on_delete=models.PROTECT)