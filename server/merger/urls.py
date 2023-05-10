from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from merger import views
from merger.views import TransactionsListView, TransactionsMergeCreateView, TransactionCategoryListCreateView, \
    TransactionCategoryMatcherListCreateView, TransactionCategoryStatsView, TransactionLogRegexMatchListView, \
    TransactionDetailView, TransactionsCSVExportView

urlpatterns = [
    path('upload/', views.upload, name='merger-upload'),
    path('categories/rematch/', views.rematch_categories, name='rematch-categories'),
    path('categories/stats/', csrf_exempt(TransactionCategoryStatsView.as_view()), name='categories-stats'),
    path('categories/', csrf_exempt(TransactionCategoryListCreateView.as_view()), name='categories'),
    path('categories/matchers/', csrf_exempt(TransactionCategoryMatcherListCreateView.as_view()), name='categories-matchers'),
    path('transactions/', csrf_exempt(TransactionsListView.as_view()), name='merger-transactions'),
    path('transactions/regex-match/', csrf_exempt(TransactionLogRegexMatchListView.as_view()), name='merger-transactions-regex-match'),
    path('transactions/<int:pk>/', csrf_exempt(TransactionDetailView.as_view()), name='merger-transaction-details'),
    path('transactions/export/', csrf_exempt(TransactionsCSVExportView.as_view()), name='transactions-export'),
    path('merge/', csrf_exempt(TransactionsMergeCreateView.as_view()), name='merger-merge')
]
