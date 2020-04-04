from django.urls.conf import path
from . import views

app_name = 'authentication'
urlpatterns = [
    path('user/add', views.CrearUsuarioView.as_view(), name='new_user'),
]

