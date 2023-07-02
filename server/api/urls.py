from django.urls import path

from api.views import TransactionsListView, TransactionsMergeCreateView, TransactionCategoryListCreateView, \
    TransactionCategoryMatcherListCreateView, TransactionCategoryStatsView, TransactionLogRegexMatchListView, \
    TransactionDetailView, TransactionsCSVExportView, UploadAPIView, CategoryRematchView, UploadVariantsListView, CategoryRemovalView

urlpatterns = [
    path('categories/', TransactionCategoryListCreateView.as_view(), name='categories'),
    path('categories/matchers/', TransactionCategoryMatcherListCreateView.as_view(), name='categories-matchers'),
    path('categories/rematch/', CategoryRematchView.as_view(), name='categories-rematch'),
    path('categories/stats/', TransactionCategoryStatsView.as_view(), name='categories-stats'),
    path('transactions/', TransactionsListView.as_view(), name='transactions'),
    path('transactions/<int:pk>/', TransactionDetailView.as_view(), name='transaction-details'),
    path('categories/remove/', CategoryRemovalView.as_view(), name='category-removal'),
    path('transactions/upload/', UploadAPIView.as_view(), name='upload'),
    path('transactions/upload/parsers/', UploadVariantsListView.as_view(), name='upload-parsers-list'),
    path('transactions/regex-match/', TransactionLogRegexMatchListView.as_view(), name='transactions-matching-regex'),
    path('transactions/export/', TransactionsCSVExportView.as_view(), name='transactions-export'),
    path('transactions/merge/', TransactionsMergeCreateView.as_view(), name='transactions-merge')
]
