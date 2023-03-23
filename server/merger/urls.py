from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from merger import views
from merger.views import TransactionsListView

urlpatterns = [
    path('upload/', views.upload, name='merger-upload'),
    path('transactions/', csrf_exempt(TransactionsListView.as_view()), name='merger-transactions'),
    path('merge/', views.merge, name='merger-merge')
]
