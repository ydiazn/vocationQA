from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from . import forms, models

# Create your views here.
class QuestionCreateView(LoginRequiredMixin, CreateView):
    form_class = forms.QuestionForm
    template_name = 'qa/ask.html'

    def get_initial(self): 
        return {
            'user': self.request.user.id
        }


class QuestionDetailView(DetailView):
    model = models.Question
    template_name = 'qa/detail.html'
    query_pk_and_slug = True