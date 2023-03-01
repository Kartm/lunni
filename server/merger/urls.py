from django.urls import path
from merger import views

urlpatterns = [
    path('', views.home, name='merger-home')
]
