import uuid as uuid_lib
from django.db import models
from django.conf import settings
from django.urls.base import reverse
from django.utils.text import slugify
from model_utils.models import TimeStampedModel

# Create your models here.
class Question(TimeStampedModel):
    slug = models.SlugField(editable=False, max_length=150)
    title = models.CharField(max_length=150)
    body = models.TextField()
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('qa:detail', kwargs={'pk': self.pk, 'slug': self.slug})
