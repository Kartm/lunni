from django.urls import path
from files import views

urlpatterns = [
    path('', views.home, name='files-home')
]
