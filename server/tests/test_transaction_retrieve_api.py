import urllib
from datetime import date

from django.urls import reverse
from rest_framework.test import APITestCase

from api.factories import TransactionFactory, CategoryFactory


class TestTransactionRetrieveAPI(APITestCase):
    def test_get_transactions(self):
        category = CategoryFactory.create()
        TransactionFactory.create(id=1, amount=300, category=category)
        TransactionFactory.create(id=2, amount=-50, category=category)

        url = reverse('transactions')

        response = self.client.get(url, {'page_size': 100})
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

    def test_get_categories_stats(self):
        income_category = CategoryFactory.create(name="Income", variant="POS")
        food_category = CategoryFactory.create(name="Food", variant="NEG")
        rent_category = CategoryFactory.create(name="Rent", variant="NEG")

        TransactionFactory.create(id=1, amount=500, category=income_category)
        TransactionFactory.create(id=2, amount=-50, category=food_category)
        TransactionFactory.create(id=3, amount=-15, category=food_category)
        TransactionFactory.create(id=4, amount=-2000, category=rent_category)
        TransactionFactory.create(id=5, amount=1, category=None)

        url = reverse('categories-stats')

        response = self.client.get(url, {'page_size': 100})
        response_json = response.json()

        self.assertEqual(len(response_json), 4)
        category_1, category_2, category_3, category_4 = response_json

        self.assertIsNone(category_1['categoryName'])
        self.assertEqual(category_1['totalCount'], 1)

        self.assertEqual(category_2['categoryName'], income_category.name)
        self.assertEqual(category_2['totalCount'], 1)

        self.assertEqual(category_3['categoryName'], food_category.name)
        self.assertEqual(category_3['totalCount'], 2)

        self.assertEqual(category_4['categoryName'], rent_category.name)
        self.assertEqual(category_4['totalCount'], 1)

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

        income_transactions = self.client.get(url, {'page_size': 100, 'category': income_category.name})
        income_transactions_json = income_transactions.json()
        self.assertEqual(income_transactions_json['count'], 1)
        income_1 = income_transactions_json['results'][0]
        self.assertEqual(income_1['id'], 1)
        self.assertEqual(income_1['calculated_amount'], 500)
        self.assertEqual(income_1['category']['name'], income_category.name)
        self.assertEqual(income_1['category']['variant'], income_category.variant)

        food_transactions = self.client.get(url, {'page_size': 100, 'category': food_category.name})
        food_transactions_json = food_transactions.json()
        self.assertEqual(food_transactions_json['count'], 2)
        food_2, food_1 = food_transactions_json['results']
        self.assertEqual(food_2['id'], 3)
        self.assertEqual(food_2['calculated_amount'], -15)
        self.assertEqual(food_2['category']['name'], food_category.name)
        self.assertEqual(food_2['category']['variant'], food_category.variant)
        self.assertEqual(food_1['id'], 2)
        self.assertEqual(food_1['calculated_amount'], -50)
        self.assertEqual(food_1['category']['name'], food_category.name)
        self.assertEqual(food_1['category']['variant'], food_category.variant)

        rent_transactions = self.client.get(url, {'page_size': 100, 'category': rent_category.name})
        rent_transactions_json = rent_transactions.json()
        self.assertEqual(rent_transactions_json['count'], 1)
        rent_1, = rent_transactions_json['results']
        self.assertEqual(rent_1['id'], 4)
        self.assertEqual(rent_1['calculated_amount'], -2000)
        self.assertEqual(rent_1['category']['name'], rent_category.name)
        self.assertEqual(rent_1['category']['variant'], rent_category.variant)

        uncategorized_transactions = self.client.get(url, {'page_size': 100, 'category': 'None'})
        uncategorized_transactions_json = uncategorized_transactions.json()
        self.assertEqual(uncategorized_transactions_json['count'], 1)
        uncategorized_1, = uncategorized_transactions_json['results']
        self.assertEqual(uncategorized_1['id'], 5)
        self.assertEqual(uncategorized_1['calculated_amount'], 1)
        self.assertIsNone(uncategorized_1['category'])

    def test_get_transactions_filter_by_multiple_categories(self):
        income_category = CategoryFactory.create(name="Income", variant="POS")
        food_category = CategoryFactory.create(name="Food", variant="NEG")

        TransactionFactory.create(id=1, amount=500, category=income_category)
        TransactionFactory.create(id=2, amount=-50, category=food_category)
        TransactionFactory.create(id=3, amount=-15, category=food_category)
        TransactionFactory.create(id=4, amount=1, category=None)

        url = reverse('transactions')

        transactions = self.client.get(url, {'page_size': 100, 'category': [income_category.name, food_category.name]})
        transactions_json = transactions.json()
        self.assertEqual(transactions_json['count'], 3)
        food_transaction_2, food_transaction_1, income_transaction = transactions_json['results']
        self.assertEqual(food_transaction_2['id'], 3)
        self.assertEqual(food_transaction_2['calculated_amount'], -15)
        self.assertEqual(food_transaction_2['category']['name'], food_category.name)
        self.assertEqual(food_transaction_2['category']['variant'], food_category.variant)

        self.assertEqual(food_transaction_1['id'], 2)
        self.assertEqual(food_transaction_1['calculated_amount'], -50)
        self.assertEqual(food_transaction_1['category']['name'], food_category.name)
        self.assertEqual(food_transaction_1['category']['variant'], food_category.variant)

        self.assertEqual(income_transaction['id'], 1)
        self.assertEqual(income_transaction['calculated_amount'], 500)
        self.assertEqual(income_transaction['category']['name'], income_category.name)
        self.assertEqual(income_transaction['category']['variant'], income_category.variant)

    def test_get_transactions_filter_by_category_and_uncategorized(self):
        income_category = CategoryFactory.create(name="Income", variant="POS")

        TransactionFactory.create(id=1, amount=500, category=income_category)
        TransactionFactory.create(id=2, amount=1, category=None)

        url = reverse('transactions')

        transactions = self.client.get(url, {'page_size': 100, 'category': [income_category.name, 'None']})
        transactions_json = transactions.json()
        self.assertEqual(transactions_json['count'], 2)
        uncategorized_transaction, income_transaction = transactions_json['results']

        self.assertEqual(uncategorized_transaction['id'], 2)
        self.assertEqual(uncategorized_transaction['calculated_amount'], 1)
        self.assertIsNone(uncategorized_transaction['category'])

        self.assertEqual(income_transaction['id'], 1)
        self.assertEqual(income_transaction['calculated_amount'], 500)
        self.assertEqual(income_transaction['category']['name'], income_category.name)
        self.assertEqual(income_transaction['category']['variant'], income_category.variant)

    def test_get_transactions_filter_by_date_range(self):
        TransactionFactory.create(id=1, category=None, date='2023-01-01')
        TransactionFactory.create(id=2, category=None, date='2023-01-02')
        TransactionFactory.create(id=3, category=None, date='2023-01-03')
        TransactionFactory.create(id=4, category=None, date='2023-01-04')
        TransactionFactory.create(id=5, category=None, date='2023-01-05')

        url = reverse('transactions')

        # inclusive
        transactions = self.client.get(url, {'date_after': '2023-01-02', 'date_before': '2023-01-04'})
        transactions_json = transactions.json()
        self.assertEqual(transactions_json['count'], 3)
        transaction_4, transaction_3, transaction_2 = transactions_json['results']

        self.assertEqual(transaction_2['id'], 2)
        self.assertEqual(transaction_3['id'], 3)
        self.assertEqual(transaction_4['id'], 4)

    def test_get_transactions_order_by_date_asc(self):
        TransactionFactory.create(id=1, category=None, date=date(2022, 12, 25))
        TransactionFactory.create(id=2, category=None, date=date(2022, 12, 26))

        url = reverse('transactions')

        transactions = self.client.get(url, {'page_size': 100, 'ordering': 'date'})
        transactions_json = transactions.json()
        self.assertEqual(transactions_json['count'], 2)
        transaction_1, transaction_2 = transactions_json['results']

        self.assertEqual(transaction_1['id'], 1)
        self.assertEqual(transaction_1['date'], '2022-12-25')
        self.assertEqual(transaction_2['id'], 2)
        self.assertEqual(transaction_2['date'], '2022-12-26')

    def test_get_transactions_order_by_date_desc(self):
        TransactionFactory.create(id=1, category=None, date=date(2022, 12, 25))
        TransactionFactory.create(id=2, category=None, date=date(2022, 12, 26))

        url = reverse('transactions')

        transactions = self.client.get(url, {'page_size': 100, 'ordering': '-date'})
        transactions_json = transactions.json()
        self.assertEqual(transactions_json['count'], 2)
        transaction_1, transaction_2 = transactions_json['results']

        self.assertEqual(transaction_1['id'], 2)
        self.assertEqual(transaction_1['date'], '2022-12-26')
        self.assertEqual(transaction_2['id'], 1)
        self.assertEqual(transaction_2['date'], '2022-12-25')

    def test_get_transactions_order_by_calculated_amount_asc(self):
        TransactionFactory.create(id=1, category=None, amount=1)
        TransactionFactory.create(id=2, category=None, amount=2)

        url = reverse('transactions')

        transactions = self.client.get(url, {'page_size': 100, 'ordering': 'calculated_amount'})
        transactions_json = transactions.json()
        self.assertEqual(transactions_json['count'], 2)
        transaction_1, transaction_2 = transactions_json['results']

        self.assertEqual(transaction_1['id'], 1)
        self.assertEqual(transaction_1['amount'], 1)
        self.assertEqual(transaction_2['id'], 2)
        self.assertEqual(transaction_2['amount'], 2)

    def test_get_transactions_order_by_calculated_amount_desc(self):
        TransactionFactory.create(id=1, category=None, amount=1)
        TransactionFactory.create(id=2, category=None, amount=2)

        url = reverse('transactions')

        transactions = self.client.get(url, {'page_size': 100, 'ordering': '-calculated_amount'})
        transactions_json = transactions.json()
        self.assertEqual(transactions_json['count'], 2)
        transaction_1, transaction_2 = transactions_json['results']

        self.assertEqual(transaction_1['id'], 2)
        self.assertEqual(transaction_1['amount'], 2)
        self.assertEqual(transaction_2['id'], 1)
        self.assertEqual(transaction_2['amount'], 1)

    def test_get_transactions_search_by_regex(self):
        TransactionFactory.create(category=None, description='Visit to a restaurant\'s')
        TransactionFactory.create(category=None, description='Visit to some museum')
        TransactionFactory.create(category=None, description='foo')

        url = reverse('transactions')

        transactions = self.client.get(url, {'page_size': 100, 'search': 'Visit to'})
        transactions_json = transactions.json()
        self.assertEqual(transactions_json['count'], 2)
        transaction_1, transaction_2 = transactions_json['results']

        self.assertEqual(transaction_1['description'], 'Visit to some museum')
        self.assertEqual(transaction_2['description'], 'Visit to a restaurant\'s')

    def test_get_transactions_search_by_regex_escaped_reserved_char(self):
        TransactionFactory.create(category=None, description='Some transaction using * in description')
        TransactionFactory.create(category=None, description='Here\'s your $$$ bro')
        TransactionFactory.create(category=None, description='foo')

        url = reverse('transactions')

        transactions = self.client.get(url, {'page_size': 100, 'search': '\*'})
        transactions_json = transactions.json()
        self.assertEqual(transactions_json['count'], 1)
        transaction_1, = transactions_json['results']

        self.assertEqual(transaction_1['description'], 'Some transaction using * in description')

    def test_get_transactions_search_by_complex_regex(self):
        TransactionFactory.create(category=None, date='2023-01-05', description='CompCo')
        TransactionFactory.create(category=None, date='2023-01-05', description='Polex')
        TransactionFactory.create(category=None, date='2023-01-07', description='Polex')
        TransactionFactory.create(category=None, description='foo')

        url = reverse('transactions')

        params = {'page_size': 100, 'search': '2023-01-05 (CompCo|Polex)'}
        transactions = self.client.get(url, params)
        transactions_json = transactions.json()
        self.assertEqual(transactions_json['count'], 2)
        transaction_1, transaction_2 = transactions_json['results']

        self.assertEqual(transaction_1['description'], 'Polex')
        self.assertEqual(transaction_2['description'], 'CompCo')

    def test_get_transactions_with_pagination(self):
        for i in range(10):
            TransactionFactory.create(category=None, amount=1)

        url = reverse('transactions')

        transactions = self.client.get(url, {'page': 1, 'page_size': 2})
        transactions_json = transactions.json()
        self.assertEqual(len(transactions_json['results']), 2)

    def test_get_transactions_without_pagination(self):
        transactions_number = 500

        TransactionFactory.create_batch(size=transactions_number, category=None, amount=1)

        url = reverse('transactions')

        transactions = self.client.get(url)
        transactions_json = transactions.json()

        # note a different response than in the paginated case
        self.assertEqual(len(transactions_json), transactions_number)
