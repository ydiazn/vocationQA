from django.urls.conf import path
from . import views


app_name = 'qa'
urlpatterns = [
    path('question/add/', views.QuestionCreateView.as_view(), name='ask'),
    path(
        'question/<int:pk>/<slug:slug>/',
        views.QuestionDetailView.as_view(),
        name='detail'
    ),
    path(
        'answer/acceptance/<int:pk>/<slug:slug>/',
        views.acceptance_answer,
        name='acceptance_answer'
    ),
    path(
        'question/reply/<int:pk>/<slug:slug>/',
        views.reply,
        name='reply'
    )
]

