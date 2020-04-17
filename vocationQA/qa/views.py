from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Sum
from django.http import HttpResponseRedirect
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView

from . import models
from . import forms


class IndexView(ListView):
    '''
    Listado de las discusiones
    '''

    def get_queryset(self):
        '''
        Redefinicion del queryset por defecto

        Se incluye al queryset el campo respuestas__count cuyo valor
        se corresponde con la cantidad de respuestas que tiene la
        pregunta asociada a la discusion
        '''
        queryset = models.Discusion.objects.annotate(
            Count('respuestas'),
        )
        # Optimizacion: reduccion de las consultas SQL necesarias para
        # para obtener la informacion de la pregunta aasociada a la discusion.
        # https://docs.djangoproject.com/en/3.0/ref/models/querysets/#select-related
        queryset = queryset.select_related('pregunta', 'pregunta__autor')
        return queryset


class CrearPreguntaView(LoginRequiredMixin, CreateView):
    form_class = forms.PreguntaForm
    template_name = 'qa/pregunta_form.html'

    def get_success_url(self):
        return reverse('qa:index')

    def get_initial(self):
        return {
            'autor': self.request.user.id,
        }


class DetalleDiscusionView(DetailView):
    queryset = models.Discusion.objects.annotate(Count('respuestas'))
    slug_field = 'pregunta__slug'
    query_pk_and_slug = True
