import csv
from collections import Counter
from io import BytesIO

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import Q, Value, CharField
from django.db.models.functions import Concat
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.views import View
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView, ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Transaction, TransactionMerge, CategoryMatcher, Category
from api.parsers import parse_mbank_statement_file, Entry, parse_pko_statement_file, \
    parse_mbank_savings_statement_file
from api.serializers import TransactionSerializer, TransactionMergeSerializer, TransactionCategorySerializer, \
    TransactionCategoryMatcherSerializer, TransactionExportSerializer


class UploadAPIView(CreateAPIView):
    function_map = {
        'mbank': parse_mbank_statement_file,
        'mbank-savings': parse_mbank_savings_statement_file,
        'pko': parse_pko_statement_file
    }

    def create(self, request, *args, **kwargs):
        variant: str = request.POST.get('variant')
        if variant not in self.function_map.keys():
            return HttpResponseBadRequest(
                f"Invalid parameter 'variant'. Allowed values are: {', '.join(self.function_map.keys())}.")

        in_memory_file: InMemoryUploadedFile = request.FILES.get('file')
        if in_memory_file is None:
            return HttpResponseBadRequest("Missing file 'file'.")

        bytes_io: BytesIO = in_memory_file.file
        extracted_entries: list[Entry] = self.function_map.get(variant)(bytes_io)

        transaction_logs_to_create = []

        for entry in extracted_entries:
            #  because admin_objects don't exclude any entries unlike TransactionsMergedManager, it's a source of truth
            if not Transaction.admin_objects.filter(
                Q(date=entry['date']) &
                Q(description=entry['description']) &
                Q(account=entry['account']) &
                Q(amount=entry['amount'])
            ).exists():
                transaction_logs_to_create.append(
                    Transaction(
                        date=entry['date'],
                        description=entry['description'],
                        account=entry['account'],
                        amount=entry['amount'],
                    )
                )

        Transaction.objects.bulk_create(transaction_logs_to_create)

        return JsonResponse(
            data={'new_entries': len(transaction_logs_to_create)},
            status=status.HTTP_201_CREATED,
        )


class TransactionsListView(ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class TransactionDetailView(RetrieveUpdateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class TransactionCategoryListCreateView(ListCreateAPIView):
    queryset = Category.objects.all().order_by('-created')
    serializer_class = TransactionCategorySerializer
    page_size = 1000


class TransactionCategoryMatcherListCreateView(ListCreateAPIView):
    queryset = CategoryMatcher.objects.all().order_by('-created')
    serializer_class = TransactionCategoryMatcherSerializer
    page_size = 1000


class TransactionsMergeCreateView(CreateAPIView):
    queryset = TransactionMerge.objects.all()
    serializer_class = TransactionMergeSerializer


class CategoryRematchView(CreateAPIView):
    def post(self, request, *args, **kwargs):
        Transaction.objects.update(category=None)

        # this is not optimal, but it's a rarely used feature so I'm leaving it as it is
        for matcher in CategoryMatcher.objects.all():
            queryset = Transaction.objects.annotate(
                search_field=Concat('date', Value(' '), 'description', output_field=CharField()))
            queryset.filter(search_field__iregex=matcher.regex_expression).update(category=matcher.category)

        return JsonResponse(
            data={},
            status=status.HTTP_200_OK,
        )


class TransactionCategoryStatsView(APIView):
    def get(self, request):
        qs = Transaction.objects.all()

        count_summary = [{'categoryName': count[0], 'totalCount': count[1]} for count in
                         Counter(list(qs.values_list('category__name', flat=True))).items()]

        return Response(count_summary)


class TransactionLogRegexMatchListView(ListAPIView):
    serializer_class = TransactionSerializer

    def get_queryset(self):
        regex_expression = self.request.query_params.get('regex_expression')

        qs = Transaction.objects.all().annotate(
            search_field=Concat('date', Value(' '), 'description', output_field=CharField())
        )
        return qs.filter(search_field__iregex=regex_expression)


class TransactionsCSVExportView(View):
    serializer_class = TransactionExportSerializer

    def get_serializer(self, queryset, many=True):
        return self.serializer_class(
            queryset,
            many=many,
        )

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="export.csv"'

        serializer = self.get_serializer(
            Transaction.objects.all(),
            many=True
        )
        header = TransactionExportSerializer.Meta.fields

        writer = csv.DictWriter(response, fieldnames=header)
        writer.writeheader()
        for row in serializer.data:
            writer.writerow(row)

        return response
