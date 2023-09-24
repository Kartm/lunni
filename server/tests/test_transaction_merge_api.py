from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.utils import json

from api.factories import TransactionFactory, CategoryFactory


class TestTransactionMergeAPI(APITestCase):
    def test_merge_transactions(self):
        category = CategoryFactory.create()
        TransactionFactory(id=1, amount=300, category=category)
        TransactionFactory(id=2, amount=-50, category=category)
        TransactionFactory(id=3, amount=100, category=category)
        TransactionFactory(id=4, amount=-100, category=category)

        url = reverse('transactions-merge')

        response = self.client.post(
            path=url,
            data=json.dumps(
                {
                    'from_transaction': 1,
                    'to_transaction': 2,
                    'amount': 49
                }
            ),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(
            path=url,
            data=json.dumps(
                {
                    'from_transaction': 3,
                    'to_transaction': 4,
                    'amount': 100
                }
            ),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = reverse('transactions')

        response_json = self.client.get(path=url).json()

        self.assertEqual(response_json['count'], 2)
        self.assertEqual(response_json['total_pages'], 1)
        self.assertEqual(response_json['results'][0]['id'], 2)
        self.assertEqual(response_json['results'][0]['calculated_amount'], -1)
        self.assertEqual(response_json['results'][1]['id'], 1)
        self.assertEqual(response_json['results'][1]['calculated_amount'], 251)

    def test_merge_transactions_prevent_negative_amount(self):
        category = CategoryFactory.create()
        TransactionFactory(id=1, amount=300, category=category)
        TransactionFactory(id=2, amount=-50, category=category)

        url = reverse('transactions-merge')

        response = self.client.post(
            path=url,
            data=json.dumps(
                {
                    'from_transaction': 1,
                    'to_transaction': 2,
                    'amount': -50
                }
            ),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_merge_transactions_prevent_overdraw(self):
        category = CategoryFactory.create()
        TransactionFactory(id=1, amount=300, category=category)
        TransactionFactory(id=2, amount=-50, category=category)

        url = reverse('transactions-merge')

        response = self.client.post(
            path=url,
            data=json.dumps(
                {
                    'from_transaction': 1,
                    'to_transaction': 2,
                    'amount': 350
                }
            ),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_merge_transactions_prevent_negative_overdraw(self):
        category = CategoryFactory.create()
        TransactionFactory(id=1, amount=300, category=category)
        TransactionFactory(id=2, amount=-50, category=category)

        url = reverse('transactions-merge')

        response = self.client.post(
            path=url,
            data=json.dumps(
                {
                    'from_transaction': 2,
                    'to_transaction': 1,
                    'amount': -30
                }
            ),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_merge_transactions_prevent_exceeding_target(self):
        category = CategoryFactory.create()
        TransactionFactory(id=1, amount=300, category=category)
        TransactionFactory(id=2, amount=-50, category=category)

        url = reverse('transactions-merge')

        response = self.client.post(
            path=url,
            data=json.dumps(
                {
                    'from_transaction': 1,
                    'to_transaction': 2,
                    'amount': 300
                }
            ),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_merge_multiple_transactions(self):
        category = CategoryFactory.create()
        TransactionFactory(id=1, amount=-75, category=category)
        TransactionFactory(id=2, amount=50, category=category)
        TransactionFactory(id=3, amount=25, category=category)

        url = reverse('transactions-merge')

        response = self.client.post(
            path=url,
            data=json.dumps(
                {
                    'from_transaction': 2,
                    'to_transaction': 1,
                    'amount': 25
                }
            ),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(
            path=url,
            data=json.dumps(
                {
                    'from_transaction': 3,
                    'to_transaction': 1,
                    'amount': 25
                }
            ),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = reverse('transactions')

        response_json = self.client.get(path=url).json()

        self.assertEqual(response_json['count'], 2)
        self.assertEqual(response_json['total_pages'], 1)
        self.assertEqual(response_json['results'][0]['id'], 2)
        self.assertEqual(response_json['results'][0]['calculated_amount'], 25)
        self.assertEqual(response_json['results'][1]['id'], 1)
        self.assertEqual(response_json['results'][1]['calculated_amount'], -25)
