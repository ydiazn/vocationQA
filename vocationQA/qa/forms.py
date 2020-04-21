from django import forms

from . import models


class PreguntaForm(forms.ModelForm):

    class Meta:
        model = models.Pregunta
        fields = ['titulo', 'cuerpo', 'autor']
        widgets = {
            'autor': forms.HiddenInput(),
        }


class RespuestaForm(forms.ModelForm):

    class Meta:
        model = models.Respuesta
        fields = ['cuerpo', 'autor', 'discusion']
        widgets = {
            'autor': forms.HiddenInput(),
            'discusion': forms.HiddenInput()
        }