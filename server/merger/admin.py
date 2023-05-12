from django.contrib import admin

from merger.models import TransactionCategoryMatcher, TransactionCategory, TransactionLog, TransactionLogMerge


class TransactionLogAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.admin_manager.all()
        return qs


admin.site.register(TransactionCategory)
admin.site.register(TransactionCategoryMatcher)
admin.site.register(TransactionLog, TransactionLogAdmin)
admin.site.register(TransactionLogMerge)
