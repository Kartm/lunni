from django.urls import path
from api import views
from api.views import TransactionsListView, TransactionsMergeCreateView, TransactionCategoryListCreateView, \
    TransactionCategoryMatcherListCreateView, TransactionCategoryStatsView, TransactionLogRegexMatchListView, \
    TransactionDetailView, TransactionsCSVExportView, UploadAPIView, CategoryRematchView

urlpatterns = [
    path('categories/', TransactionCategoryListCreateView.as_view(), name='categories'),
    path('categories/matchers/', TransactionCategoryMatcherListCreateView.as_view(), name='categories-matchers'),
    path('categories/rematch/', CategoryRematchView.as_view(), name='rematch-categories'),
    path('categories/stats/', TransactionCategoryStatsView.as_view(), name='categories-stats'),
    path('transactions/', TransactionsListView.as_view(), name='merger-transactions'),
    path('transactions/<int:pk>/', TransactionDetailView.as_view(), name='merger-transaction-details'),
    path('transactions/upload/', UploadAPIView.as_view(), name='merger-upload'),
    path('transactions/regex-match/', TransactionLogRegexMatchListView.as_view(), name='merger-transactions-regex-match'),
    path('transactions/export/', TransactionsCSVExportView.as_view(), name='transactions-export'),
    path('transactions/merge/', TransactionsMergeCreateView.as_view(), name='merger-merge')
]
