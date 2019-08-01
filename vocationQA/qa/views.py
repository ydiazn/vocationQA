from django.shortcuts import render
from django.urls import reverse
from django import http
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from . import forms, models


# Create your views here.
class QuestionListView(ListView):
    template_name = 'qa/questions.html'
    model = models.Question


class QuestionCreateView(LoginRequiredMixin, CreateView):
    form_class = forms.QuestionForm
    template_name = 'qa/ask.html'

    '''
    view.get_initial() => dict: get_initial method redefinition
    for setting question form user to authenticated user
    '''
    def get_initial(self): 
        return {
            'user': self.request.user.id
        }


class QuestionDetailView(DetailView):
    model = models.Question
    template_name = 'qa/detail.html'
    query_pk_and_slug = True

    # forms
    accept_answer_form = forms.AnswerAceptanceForm(initial={'accepted': True})
    reject_answer_form = forms.AnswerAceptanceForm(initial={'accepted': False})

    def get_answers(self):
        '''
        view.get_answer(question) => queryset: return all answers
        of question
        '''
        return self.object.answer_set.all()

    def get_create_answer_form(self):
        return forms.AnswerForm(initial={
            'user': self.request.user,
            'question': self.object
        })

    def get_context_data(self, **kwargs):
        '''
        view.get_context_data(...) => dict: get_context_data
        redefinition to add extra data needed.
        '''
        context = super().get_context_data(**kwargs)
        answers = self.get_answers()
        can_accept_answer = self.object.user_can_accept_answer(self.request.user)
        
        context.update({
            'answers': answers,
            'can_accept_answer': can_accept_answer,
        })
        # Only send create answer form if user is authenticated
        if self.request.user.is_authenticated:
            context.update({
                'create_answer_form': self.get_create_answer_form()
            })
        # Only send forms if user can accept and reject answers
        if can_accept_answer:
            context.update({
                'accept_answer_form': self.accept_answer_form,
                'reject_answer_form': self.reject_answer_form,
            })

        return context


@login_required
def acceptance_answer(request, pk, slug):
    answer = get_object_or_404(models.Answer, pk=pk, slug=slug)
    question = answer.question

    if request.method == 'POST':
        form = forms.AnswerAceptanceForm(request.POST, instance=answer)
        if form.is_valid():
            form.save()
            return http.HttpResponseRedirect(
                reverse(
                    'qa:detail',
                    kwargs={'pk': question.pk, 'slug': question.slug}
                )
            )
        else:
            return http.HttpResponseForbidden()
    else:
        return http.HttpResponseNotAllowed(['GET'])


@login_required
def reply(request, pk, slug):
    question = get_object_or_404(models.Question, pk=pk, slug=slug)

    if request.method == 'POST':
        form = forms.AnswerForm(request.POST)
        if form.is_valid():
            form.save()
            return http.HttpResponseRedirect(
                reverse(
                    'qa:detail',
                    kwargs={'pk': question.pk, 'slug': question.slug}
                )
            )
        else:
            return http.HttpResponseForbidden()
    else:
        return http.HttpResponseNotAllowed(['GET'])