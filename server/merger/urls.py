from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from merger import views
from merger.views import TransactionsListView, TransactionsMergeCreateView

urlpatterns = [
    path('upload/', views.upload, name='merger-upload'),
    path('categories/rematch', views.rematch_categories, name='rematch-categories'),
    path('transactions/', csrf_exempt(TransactionsListView.as_view()), name='merger-transactions'),
    path('merge/', csrf_exempt(TransactionsMergeCreateView.as_view()), name='merger-merge')
]
