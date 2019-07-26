from django.urls import include, path
import debug_toolbar
from .base import urlpatterns

urlpatterns = [
    path('__debug__/', include(debug_toolbar.urls)),
] + urlpatterns