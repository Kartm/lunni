from io import BytesIO

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView

from merger.helpers import file_to_entries
from merger.models import TransactionLog, TransactionLogMerge
from merger.serializers import TransactionLogSerializer, TransactionLogMergeSerializer, CreateTransactionLogSerializer


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
        data={},
        status=status.HTTP_201_CREATED,
    )


class TransactionsListView(ListAPIView):
    queryset = TransactionLog.objects.all()
    serializer_class = TransactionLogSerializer


class TransactionsMergeCreateView(CreateAPIView):
    queryset = TransactionLogMerge.objects.all()
    serializer_class = TransactionLogMergeSerializer
