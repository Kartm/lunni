import re
from io import BytesIO

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import Count, Max, F, Q
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
    queryset = TransactionLog.objects.all().order_by('-date', 'amount')
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
        TransactionLog.objects.filter(description__iregex=matcher.regex_expression).update(category=matcher.category)

    return JsonResponse(
        data={},
        status=status.HTTP_200_OK,
    )


class TransactionCategoryStatsView(APIView):
    def get(self, request):
        # todo case... use a serializer to handle that
        qs = TransactionLog.objects.values(categoryName=F('category__name')).annotate(totalCount=Count('pk'))

        return Response([dict(q) for q in qs])


class TransactionLogRegexMatchListView(ListAPIView):
    serializer_class = TransactionLogSerializer
    # todo add limited serializer for better performance

    def get_queryset(self):
        queryset = TransactionLog.objects.all()
        regex_expression = self.request.query_params.get('regex_expression')
        return queryset.filter(description__iregex=regex_expression)
