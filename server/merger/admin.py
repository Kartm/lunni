from django.contrib import admin

from merger.models import TransactionCategoryMatcher, TransactionCategory, TransactionLog, TransactionLogMerge

admin.site.register(TransactionCategory)
admin.site.register(TransactionCategoryMatcher)
admin.site.register(TransactionLog)
admin.site.register(TransactionLogMerge)

