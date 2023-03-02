import json
from decimal import Decimal

import pandas as pd
from django.core.exceptions import BadRequest
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from rest_framework import status

from merger.models import TransactionLog
from merger.serializers import TransactionLogSerializer, TransactionLogMergeSerializer


@require_POST
@csrf_exempt
def upload(request, *args, **kwargs):
    in_memory_file = request.FILES.get('file')
    bytes_io = in_memory_file.file
    df = pd.read_csv(bytes_io, skiprows=25, sep=';', index_col=False,)

    # take only necessary columns
    df = df.iloc[:, :5]

    # rename headers
    df = df.rename(
        columns={
            '#Data operacji': 'Date',
            '#Opis operacji': 'Description',
            '#Rachunek': 'Account',
            '#Kategoria': 'Category',
            '#Kwota': 'Amount',
        }
    )

    # parse 'Amount' column
    # e.g. 7 921,39 PLN -> 7921.39
    # todo improve performance
    df['Amount'] = df['Amount'].apply(
        lambda amount:
        amount.replace("PLN", "")
        .replace(",", "")
        .replace(" ", "")
    ).astype(int)

    converted_entries = df.rename(
        columns={
            'Date': 'date',
            'Description': 'description',
            'Account': 'account',
            'Category': 'category',
            'Amount': 'amount',
        }
    ).to_dict('records')

    serializer = TransactionLogSerializer(data=converted_entries, many=True)
    serializer.is_valid()
    serializer.save()

    response_data = {
        'loaded_rows': serializer.data
    }

    return JsonResponse(
        response_data,
        status=status.HTTP_201_CREATED,
    )

@require_GET
@csrf_exempt
def transactions(request, *args, **kwargs):
    data = TransactionLog.objects.all()
    serializer = TransactionLogSerializer(data=data, many=True)
    serializer.is_valid()

    response_data = {
        'transactions': serializer.data
    }

    return JsonResponse(
        response_data,
        status=status.HTTP_200_OK,
    )

@require_POST
@csrf_exempt
def merge(request, *args, **kwargs):
    body = json.loads(request.body.decode('utf-8'))

    serializer = TransactionLogMergeSerializer(data=body)
    serializer.is_valid()

    from_transaction_serialized = TransactionLogSerializer(
        serializer.validated_data.get('from_transaction')
    )

    attempted_amount_transfer = serializer.validated_data.get('amount')
    available_amount = from_transaction_serialized.data.get('amount')

    if attempted_amount_transfer > available_amount:
        raise BadRequest('Cannot transfer from transaction more than the available transaction value')

    serializer.save()

    response_data = {
        'transaction_merge': serializer.data
    }

    return JsonResponse(
        response_data,
        status=status.HTTP_200_OK,
    )
