from django.urls.conf import path
from . import views

app_name = 'qa'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('qa/question/add', views.CrearPreguntaView.as_view(), name='ask'),
    path(
        'qa/question/<int:pk>/<slug:slug>/',
        views.DetalleDiscusionView.as_view(),
        name='discusion-detail'
    ),
    path(
        'qa/discusion/<int:discusion_pk>/post/<int:post_pk>/flaggin/',
        views.FlagginCreateView.as_view(),
        name='flaggin'
    ),
    path(
        'qa/discusion/<int:discusion_pk>/post/<int:post_pk>/flags/',
        views.FlagsView.as_view(),
        name='flags'
    )
]

