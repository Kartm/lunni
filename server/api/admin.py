from django.contrib import admin

from api.models import CategoryMatcher, Category, Transaction, TransactionMerge


class TransactionAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.admin_objects.all()
        return qs


admin.site.register(Category)
admin.site.register(CategoryMatcher)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(TransactionMerge)
