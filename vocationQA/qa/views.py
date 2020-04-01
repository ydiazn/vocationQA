# from django.shortcuts import render
from django.urls import reverse
# from django import http
# 
# from django.views.generic.edit import CreateView
# from django.views.generic.detail import DetailView
# from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.http import HttpResponseRedirect
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView

from . import models


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
    model = models.Pregunta
    fields = ['titulo', 'cuerpo']

    def get_success_url(self):
        return reverse('qa:index')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.autor = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
