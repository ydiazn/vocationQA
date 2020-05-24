from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Sum
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, FormMixin, UpdateView
from django.views.generic.detail import (
    DetailView, SingleObjectTemplateResponseMixin, SingleObjectMixin)
from django.views.generic.base import View

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


class DiscusionView(DetailView):
    queryset = models.Discusion.objects.annotate(Count('respuestas'))
    slug_field = 'pregunta__slug'
    query_pk_and_slug = True

    def get_form(self):
        autor = self.request.user.id
        discusion = self.object.id
        form = forms.RespuestaForm(
            initial={'autor': autor, 'discusion': discusion})

        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = {
            'answer_form': self.get_form(),
            'observaciones': self.object.pregunta.publicacion_ptr.observaciones.all()
        }
        context.update(data)
        return context


class AnswerView(
        LoginRequiredMixin, SingleObjectTemplateResponseMixin,
        SingleObjectMixin, FormMixin, View):

    queryset = models.Discusion.objects.annotate(Count('respuestas'))
    slug_field = 'pregunta__slug'
    query_pk_and_slug = True
    form_class = forms.RespuestaForm
    template_name = 'qa/discusion_detail.html'
    context_object_name = 'discusion'

    def get_success_url(self):
        '''
        Return url to redirect after success answer creation
        '''
        return reverse(
            'qa:discusion-detail',
            kwargs={'pk': self.object.pk, 'slug': self.object.pregunta.slug}
        )

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        """If the form is invalid, render object and the invalid form."""
        return self.render_to_response(self.get_context_data(form=form, object=self.object))

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        self.object = self.get_object()
        self.user = request.user

        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class DetalleDiscusionView(View):

    def get(self, request, *args, **kwargs):
        view = DiscusionView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = AnswerView.as_view()
        return view(request, *args, **kwargs)


class FlagginCreateView(LoginRequiredMixin, CreateView):

    model = models.Publicacion
    form_class = forms.FlagginForm
    template_name = 'qa/flaggin_form.html'

    def get_thread(self, **kwargs):
        return get_object_or_404(
            models.Discusion, pk=kwargs.get('discusion_pk'))
    
    def get_post(self, **kwargs):
        return get_object_or_404(
            models.Publicacion, pk=kwargs.get('post_pk'))

    def get(self, request, *args, **kwargs):
        self.publicacion = self.get_post(**kwargs)
        self.thread = self.get_thread(**kwargs)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.publicacion = self.get_post(**kwargs)
        self.thread = self.get_thread(**kwargs)
        return super().post(request, *args, **kwargs)

    def get_initial(self):
        return {
            'usuario': self.request.user.id,
            'publicacion': self.publicacion.id
        }

    def get_success_url(self):
        '''
        Return url to redirect after success answer creation
        '''
        return reverse(
            'qa:discusion-detail',
            kwargs={'pk': self.thread.pk, 'slug': self.thread.pregunta.slug}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = {'discusion': self.thread}
        context.update(data)
        return context


class FlagsView(LoginRequiredMixin, ListView):
    '''
    Listado de las discusiones
    '''

    def get(self, request, *args, **kwargs):
        self.discusion = get_object_or_404(
            models.Discusion, pk=kwargs.get('discusion_pk'))
        self.publicacion = get_object_or_404(
            models.Publicacion, pk=kwargs.get('post_pk'))
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = self.publicacion.observaciones.filter(
            observacion__usuario=self.request.user
        )
        return queryset

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data.update({'discusion': self.discusion})
        return data
