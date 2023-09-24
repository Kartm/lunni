import datetime

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.factories import TransactionFactory, CategoryFactory


class TestTransactionExportAPI(APITestCase):
    def test_export_transactions(self):
        category = CategoryFactory(
            id=1,
            name='subscriptions',
            variant='NEG'
        )

        TransactionFactory(
            id=1,
            amount=300,
            description='gift',
            date=datetime.date(2018, 5, 1),
            category=category
        )
        TransactionFactory(
            id=2,
            amount=-50,
            description='spotify payment',
            date=datetime.date(2018, 5, 6),
            category=None
        )

        url = reverse('transactions-export')

        response = self.client.get(path=url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_content = response.content.decode('utf-8')
        csv_lines = [line for line in response_content.split('\r\n') if line != '']
        header = csv_lines.pop(0)

        self.assertEqual(header, 'id,date,description,note,account,category_name,category_variant,calculated_amount')
        self.assertEqual(len(csv_lines), 2)
        self.assertEqual(csv_lines[0], '2,2018-05-06,spotify payment,,prywatnte,,,-0.50')
        self.assertEqual(csv_lines[1], '1,2018-05-01,gift,,prywatnte,subscriptions,NEG,3.00')
