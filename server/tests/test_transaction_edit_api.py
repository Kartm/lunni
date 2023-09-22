from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.utils import json

from api.factories import TransactionFactory


class TestTransactionEditAPI(APITestCase):
    def test_editing_single_transaction(self):
        TransactionFactory(id=1, amount=300)

        url = reverse('transaction-details', kwargs={'pk': 1})

        response = self.client.get(
            path=url,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_json = response.json()

        self.assertEqual(response_json['note'], '')

        response = self.client.patch(
            path=url,
            data=json.dumps(
                {
                    'note': 'my note',
                }
            ),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_json = response.json()

        self.assertEqual(response_json['note'], 'my note')
