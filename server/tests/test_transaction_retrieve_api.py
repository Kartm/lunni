from django.urls import reverse
from rest_framework.test import APITestCase

from api.factories import TransactionFactory, CategoryFactory


class TestTransactionRetrieveAPI(APITestCase):
    def test_get_transactions(self):
        category = CategoryFactory.create()
        TransactionFactory.create(id=1, amount=300, category=category)
        TransactionFactory.create(id=2, amount=-50, category=category)

        url = reverse('transactions')

        response = self.client.get(path=url)

        response_json = response.json()

        self.assertEqual(response_json['count'], 2)
        self.assertEqual(response_json['total_pages'], 1)

        first_result = response_json['results'][0]
        self.assertEqual(first_result['id'], 2)
        self.assertEqual(first_result['amount'], -50)
        self.assertEqual(first_result['calculated_amount'], -50)
        self.assertEqual(first_result['date'], '2023-01-05')
        self.assertEqual(first_result['description'], 'desc')
        self.assertEqual(first_result['account'], 'prywatnte')
        self.assertEqual(first_result['category']['id'], 1)
        self.assertEqual(first_result['category']['name'], 'food')
        self.assertEqual(first_result['category']['variant'], 'NEG')

        second_result = response_json['results'][1]
        self.assertEqual(second_result['id'], 1)
        self.assertEqual(second_result['amount'], 300)
        self.assertEqual(second_result['calculated_amount'], 300)
        self.assertEqual(second_result['date'], '2023-01-05')
        self.assertEqual(second_result['description'], 'desc')
        self.assertEqual(second_result['account'], 'prywatnte')
        self.assertEqual(second_result['category']['id'], 1)
        self.assertEqual(second_result['category']['name'], 'food')
        self.assertEqual(second_result['category']['variant'], 'NEG')

    def test_get_transactions_filter_by_category(self):
        income_category = CategoryFactory.create(name="Income", variant="POS")
        food_category = CategoryFactory.create(name="Food", variant="NEG")
        rent_category = CategoryFactory.create(name="Rent", variant="NEG")

        TransactionFactory.create(id=1, amount=500, category=income_category)
        TransactionFactory.create(id=2, amount=-50, category=food_category)
        TransactionFactory.create(id=3, amount=-15, category=food_category)
        TransactionFactory.create(id=4, amount=-2000, category=rent_category)
        TransactionFactory.create(id=5, amount=1, category=None)

        url = reverse('transactions')

        income_transactions = self.client.get(url, {'category': income_category.name})
        income_transactions_json = income_transactions.json()
        self.assertEqual(income_transactions_json['count'], 1)
        income_1 = income_transactions_json['results'][0]
        self.assertEqual(income_1['id'], 1)
        self.assertEqual(income_1['calculated_amount'], 500)
        self.assertEqual(income_1['category']['name'], income_category.name)
        self.assertEqual(income_1['category']['variant'], income_category.variant)

        food_transactions = self.client.get(url, {'category': food_category.name})
        food_transactions_json = food_transactions.json()
        self.assertEqual(food_transactions_json['count'], 2)
        food_1, food_2 = food_transactions_json['results']
        self.assertEqual(food_1['id'], 2)
        self.assertEqual(food_1['calculated_amount'], -50)
        self.assertEqual(food_1['category']['name'], food_category.name)
        self.assertEqual(food_1['category']['variant'], food_category.variant)
        self.assertEqual(food_2['id'], 3)
        self.assertEqual(food_2['calculated_amount'], -15)
        self.assertEqual(food_2['category']['name'], food_category.name)
        self.assertEqual(food_2['category']['variant'], food_category.variant)

        rent_transactions = self.client.get(url, {'category': rent_category.name})
        rent_transactions_json = rent_transactions.json()
        self.assertEqual(rent_transactions_json['count'], 1)
        rent_1, = rent_transactions_json['results']
        self.assertEqual(rent_1['id'], 4)
        self.assertEqual(rent_1['calculated_amount'], -2000)
        self.assertEqual(rent_1['category']['name'], rent_category.name)
        self.assertEqual(rent_1['category']['variant'], rent_category.variant)

        uncategorized_transactions = self.client.get(url, {'uncategorized': True})
        uncategorized_transactions_json = uncategorized_transactions.json()
        self.assertEqual(uncategorized_transactions_json['count'], 1)
        uncategorized_1, = uncategorized_transactions_json['results']
        self.assertEqual(uncategorized_1['id'], 5)
        self.assertEqual(uncategorized_1['calculated_amount'], 1)
        self.assertIsNone(uncategorized_1['category'])
