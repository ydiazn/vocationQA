from django import forms
from django.contrib.auth import get_user_model
from . import models


class QuestionForm(forms.ModelForm):
    class Meta:
        model = models.Question
        fields = ['title', 'body', 'user']

    user = forms.ModelChoiceField(
        widget=forms.HiddenInput,
        queryset=get_user_model().objects.all(),
        disabled=False
    )