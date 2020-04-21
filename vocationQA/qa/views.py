from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Sum
from django.http import HttpResponseRedirect
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, FormMixin
from django.views.generic.detail import (
    DetailView, SingleObjectTemplateResponseMixin, SingleObjectMixin)
from django.views.generic.base import View
from authentication.views import LoginRequiredMixin as LoginRequiredMixinWithNext

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

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_form(self):
        return forms.RespuestaForm(
            initial={
                'autor': self.request.user.id,
                'discusion': self.object.id
            }
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = {'answer_form': self.get_form()}
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
