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


class FlagginForm(forms.ModelForm):

    def __init__(self, *args, **kwars):
        super().__init__(*args, **kwars)
        self.fields['flag'].empty_label = None

    class Meta:
        model = models.Observacion
        fields = ['publicacion', 'flag', 'usuario']
        widgets = {
            'flag': forms.RadioSelect,
            'usuario': forms.HiddenInput,
            'publicacion': forms.HiddenInput
        }