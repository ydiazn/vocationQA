# from django.shortcuts import render
# from django.urls import reverse
# from django import http
# 
# from django.views.generic.edit import CreateView
# from django.views.generic.detail import DetailView
# from django.shortcuts import get_object_or_404
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.views.generic.list import ListView

from . import models


class IndexView(ListView):

    def get_queryset(self):
        queryset = models.Discusion.objects.annotate(
            Count('respuestas'),
        )
        queryset = queryset.select_related('pregunta')
        return queryset
