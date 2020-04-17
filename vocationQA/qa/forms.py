from django import forms

from . import models


class PreguntaForm(forms.ModelForm):

    class Meta:
        model = models.Pregunta
        fields = ['titulo', 'cuerpo', 'autor']
        widgets = {
            'autor': forms.HiddenInput(),
        }