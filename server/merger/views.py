import re
from collections import Counter
from io import BytesIO

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import Count, Max, F, Q, Value, CharField, Sum, DecimalField, OuterRef, Subquery, Case, When, \
    IntegerField
from django.db.models.functions import Concat, Coalesce
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView, ListCreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from merger.helpers import file_to_entries
from merger.models import TransactionLog, TransactionLogMerge, TransactionCategoryMatcher, TransactionCategory
from merger.serializers import TransactionLogSerializer, TransactionLogMergeSerializer, CreateTransactionLogSerializer, \
    TransactionCategorySerializer, TransactionCategoryMatcherSerializer


@require_POST
@csrf_exempt
def upload(request, *args, **kwargs):
    in_memory_file: InMemoryUploadedFile = request.FILES.get('file')
    bytes_io: BytesIO = in_memory_file.file
    converted_entries = file_to_entries(bytes_io)

    serializer = CreateTransactionLogSerializer(data=converted_entries, many=True)
    serializer.is_valid()
    serializer.save()

    return JsonResponse(
        data={'converted_entries': converted_entries},
        status=status.HTTP_201_CREATED,
    )


class TransactionsListView(ListAPIView):
    from_sums = TransactionLogMerge.objects.filter(
        from_transaction=OuterRef('pk')
    ).annotate(s=Sum(F('amount'))).values('s')

    to_sums = TransactionLogMerge.objects.filter(
        to_transaction=OuterRef('pk')
    ).annotate(s=Sum(F('amount'))).values('s')

    queryset = TransactionLog.objects.annotate(
        calculated_amount=Coalesce(Subquery(from_sums), 0) * (-1) + Coalesce(Subquery(to_sums), 0) + F('amount'),
    ).exclude(calculated_amount__exact=0).order_by('-date', 'amount')
    serializer_class = TransactionLogSerializer


class TransactionCategoryListCreateView(ListCreateAPIView):
    queryset = TransactionCategory.objects.all().order_by('-created')
    serializer_class = TransactionCategorySerializer
    page_size = 1000


class TransactionCategoryMatcherListCreateView(ListCreateAPIView):
    queryset = TransactionCategoryMatcher.objects.all().order_by('-created')
    serializer_class = TransactionCategoryMatcherSerializer
    page_size = 1000


class TransactionsMergeCreateView(CreateAPIView):
    queryset = TransactionLogMerge.objects.all()
    serializer_class = TransactionLogMergeSerializer


@require_POST
@csrf_exempt
def rematch_categories(request, *args, **kwargs):
    TransactionLog.objects.update(category=None)


    for matcher in TransactionCategoryMatcher.objects.all():
        queryset = TransactionLog.objects.annotate(search_field=Concat('date', Value(' '), 'description', output_field=CharField()))
        queryset.filter(search_field__iregex=matcher.regex_expression).update(category=matcher.category)

    return JsonResponse(
        data={},
        status=status.HTTP_200_OK,
    )


class TransactionCategoryStatsView(APIView):
    def get(self, request):
        from_sums = TransactionLogMerge.objects.filter(
            from_transaction=OuterRef('pk')
        ).annotate(s=Sum(F('amount'))).values('s')

        to_sums = TransactionLogMerge.objects.filter(
            to_transaction=OuterRef('pk')
        ).annotate(s=Sum(F('amount'))).values('s')

        qs = TransactionLog.objects.annotate(
            calculated_amount=Coalesce(Subquery(from_sums), 0) * (-1) + Coalesce(Subquery(to_sums), 0) + F('amount'),
        ).exclude(calculated_amount__exact=0).order_by('-date', 'amount')

        count_summary = [{'categoryName': count[0], 'totalCount': count[1]} for count in Counter(list(qs.values_list('category__name', flat=True))).items()]

        return Response(count_summary)


class TransactionLogRegexMatchListView(ListAPIView):
    serializer_class = TransactionLogSerializer
    # todo add limited serializer for better performance

    def get_queryset(self):
        regex_expression = self.request.query_params.get('regex_expression')

        from_sums = TransactionLogMerge.objects.filter(
            from_transaction=OuterRef('pk')
        ).annotate(s=Sum(F('amount'))).values('s')

        to_sums = TransactionLogMerge.objects.filter(
            to_transaction=OuterRef('pk')
        ).annotate(s=Sum(F('amount'))).values('s')

        qs = TransactionLog.objects.annotate(
            calculated_amount=Coalesce(Subquery(from_sums), 0) * (-1) + Coalesce(Subquery(to_sums), 0) + F('amount'),
        ).exclude(calculated_amount__exact=0).order_by('-date', 'amount')

        qs = qs.annotate(search_field=Concat('date', Value(' '), 'description', output_field=CharField()))
        return qs.filter(search_field__iregex=regex_expression)

