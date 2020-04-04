from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.edit import CreateView

# Create your views here.


class CrearUsuarioView(CreateView):
    form_class = UserCreationForm
    template_name = 'authentication/usuario_form.html'
    
    def get_success_url(self):
        return reverse('qa:index')
