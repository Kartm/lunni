from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.urls import include, path

urlpatterns = [
    path("", include("lunni2.urls")),
]

