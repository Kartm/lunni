from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.factories import TransactionFactory, CategoryFactory, CategoryMatcherFactory


class TestTransactionRematchAPI(APITestCase):
    def test_rematch_categories(self):
        TransactionFactory(
            id=1,
            amount=300,
            description='gift',
            category=None
        )
        TransactionFactory(
            id=2,
            amount=-50,
            description='spotify payment',
            category=None
        )
        subscriptionsCategory = CategoryFactory(
            id=1,
            name='subscriptions',
            variant='NEG'
        )
        CategoryMatcherFactory(
            id=1,
            regex_expression='spotify',
            category=subscriptionsCategory
        )

        url = reverse('categories-rematch')

        response = self.client.post(
            path=url,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('transactions')

        response = self.client.get(
            path=url,
        )

        response_content = response.json()
        self.assertEqual(response_content['count'], 2)
        self.assertEqual(response_content['total_pages'], 1)

        results = response_content['results']
        self.assertEqual(len(results), 2)

        first_result = results[0]
        self.assertEqual(first_result['id'], 2)
        self.assertEqual(first_result['date'], '2023-01-05')
        self.assertEqual(first_result['description'], 'spotify payment')
        self.assertEqual(first_result['account'], 'prywatnte')
        self.assertEqual(first_result['category'], {'id': 1, 'name': 'subscriptions', 'variant': 'NEG'})
        self.assertEqual(first_result['amount'], -50)
        self.assertEqual(first_result['calculated_amount'], -50)

        second_result = results[1]
        self.assertEqual(second_result['id'], 1)
        self.assertEqual(second_result['date'], '2023-01-05')
        self.assertEqual(second_result['description'], 'gift')
        self.assertEqual(second_result['account'], 'prywatnte')
        self.assertIsNone(second_result['category'])
        self.assertEqual(second_result['amount'], 300)
        self.assertEqual(second_result['calculated_amount'], 300)
