from django.urls import path

from merger import views
from merger.views import TransactionsListView, TransactionsMergeCreateView, TransactionCategoryListCreateView, \
    TransactionCategoryMatcherListCreateView, TransactionCategoryStatsView, TransactionLogRegexMatchListView, \
    TransactionDetailView, TransactionsCSVExportView, UploadAPIView

urlpatterns = [
    path('upload/', UploadAPIView.as_view(), name='merger-upload'),
    path('categories/rematch/', views.rematch_categories, name='rematch-categories'),
    path('categories/stats/', TransactionCategoryStatsView.as_view(), name='categories-stats'),
    path('categories/', TransactionCategoryListCreateView.as_view(), name='categories'),
    path('categories/matchers/', TransactionCategoryMatcherListCreateView.as_view(), name='categories-matchers'),
    path('transactions/', TransactionsListView.as_view(), name='merger-transactions'),
    path('transactions/regex-match/', TransactionLogRegexMatchListView.as_view(), name='merger-transactions-regex-match'),
    path('transactions/<int:pk>/', TransactionDetailView.as_view(), name='merger-transaction-details'),
    path('transactions/export/', TransactionsCSVExportView.as_view(), name='transactions-export'),
    path('merge/', TransactionsMergeCreateView.as_view(), name='merger-merge')
]
