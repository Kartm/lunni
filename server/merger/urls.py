from django.urls import path
from merger import views

urlpatterns = [
    path('upload/', views.upload, name='merger-upload'),
    path('transactions/', views.transactions, name='merger-transactions'),
    path('merge/', views.merge, name='merger-merge')
]
