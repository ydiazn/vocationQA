from django import forms
from django.contrib.auth import get_user_model
from . import models


# class QuestionForm(forms.ModelForm):
#     user = forms.ModelChoiceField(
#         widget=forms.HiddenInput,
#         queryset=get_user_model().objects.all(),
#         disabled=False
#     )

#     class Meta:
#         model = models.Pregunta
#         fields = ['title', 'body', 'user']


# class AnswerAceptanceForm(forms.ModelForm):
#     accepted = forms.BooleanField(
#         widget=forms.HiddenInput,
#         required=False
#     )

#     class Meta:
#         model = models.Respuesta
#         fields = ['accepted']


# class AnswerQuestionForm(forms.ModelForm):

#     class Meta:
#         model = models.Respuesta
#         fields = ['body']