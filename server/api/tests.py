import datetime
import os
from io import BytesIO
from django.test.client import MULTIPART_CONTENT, encode_multipart, BOUNDARY
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.utils import json

from api.factories import TransactionFactory, CategoryFactory, CategoryMatcherFactory


class LunniAPITestCase(APITestCase):
    def upload_file(self, bio: BytesIO, parser: str):
        url = reverse('upload')
        return self.client.post(
            path=url,
            data=encode_multipart(
                data=dict(file=bio, parser=parser),
                boundary=BOUNDARY,
            ),
            content_type=MULTIPART_CONTENT,
        )

    def test_get_available_parsers(self):
        url = reverse('upload-parsers-list')

        response = self.client.get(path=url)

        response_json = response.json()

        self.assertEqual(response_json, [
            {'symbol': 'mbank', 'label': 'mBank'},
            {'symbol': 'mbank-savings', 'label': 'mBank Cele'},
            {'symbol': 'pko', 'label': 'PKO'},
            {'symbol': 'ing', 'label': 'ING Bank Śląski'},
        ])

    def test_upload_mbank_file(self):
        with open(os.path.join(os.path.dirname(__file__), os.pardir, 'test_resources', 'mbank_statement_file.csv'),
                  mode='rb') as f:
            bio = BytesIO(f.read())
            response = self.upload_file(bio, 'mbank')

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            response_content = response.json()['new_entries']
            self.assertEqual(response_content, 2)

    def test_upload_mbank_savings_file(self):
        with open(os.path.join(os.path.dirname(__file__), os.pardir, 'test_resources', 'mbank_statement_savings_file.csv'),
                  mode='rb') as f:
            bio = BytesIO(f.read())
            response = self.upload_file(bio, 'mbank-savings')

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            response_content = response.json()['new_entries']
            self.assertEqual(response_content, 2)

    def test_prevent_csv_duplicates(self):
        with open(os.path.join(os.path.dirname(__file__), os.pardir, 'test_resources', 'mbank_statement_duplicate_file.csv'),
                  mode='rb') as f:
            bio = BytesIO(f.read())

            response = self.upload_file(bio, 'mbank')

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            response_content = response.json()['new_entries']
            self.assertEqual(response_content, 2)

            # upload again
            f.seek(0)
            bio = BytesIO(f.read())
            response = self.upload_file(bio, 'mbank')

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            response_content = response.json()['new_entries']
            self.assertEqual(response_content, 0)

    def test_prevent_database_duplicates(self):
        category = CategoryFactory.create()
        TransactionFactory(date='2023-01-05', description='desc', account='prywatnte', amount=1, category=category)

        with open(os.path.join(os.path.dirname(__file__), os.pardir, 'test_resources', 'mbank_statement_database_duplicate_file.csv'),
                  mode='rb') as f:
            bio = BytesIO(f.read())
            response = self.upload_file(bio, 'mbank')

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            response_content = response.json()['new_entries']
            self.assertEqual(response_content, 0)

    def test_upload_pko_file(self):
        with open(os.path.join(os.path.dirname(__file__), os.pardir, 'test_resources', 'pko_statement_file.csv'),
                  mode='rb') as f:
            bio = BytesIO(f.read())
            response = self.upload_file(bio, 'pko')

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            response_content = response.json()['new_entries']
            self.assertEqual(response_content, 2)

    def test_upload_ing_file(self):
        with open(os.path.join(os.path.dirname(__file__), os.pardir, 'test_resources', 'ing_statement_file.csv'),
                  mode='rb') as f:
            bio = BytesIO(f.read())
            response = self.upload_file(bio, 'ing')

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            response_content = response.json()['new_entries']
            self.assertEqual(response_content, 3)

    def test_upload_file_compare_by_amount(self):
        with open(os.path.join(os.path.dirname(__file__), os.pardir, 'test_resources', 'mbank_statement_file.csv'),
                  mode='rb') as f:
            bio = BytesIO(f.read())

            # when uploaded two entries
            response = self.upload_file(bio, 'mbank')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            response_content = response.json()['new_entries']
            self.assertEqual(response_content, 2)

            # and when merged them
            url = reverse('transactions-merge')

            response = self.client.post(
                path=url,
                data=json.dumps(
                    {
                        'from_transaction': 1,
                        'to_transaction': 2,
                        'amount': 1580
                    }
                ),
                content_type='application/json'
            )
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

            # and when trying to upload same rows again
            f.seek(0)
            bio = BytesIO(f.read())
            response = self.upload_file(bio, 'mbank')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

            # then no entries have been added
            response_content = response.json()['new_entries']
            self.assertEqual(response_content, 0)

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
        self.assertEqual(response_json['results'][0]['id'], 1)
        self.assertEqual(response_json['results'][0]['calculated_amount'], -25)
        self.assertEqual(response_json['results'][1]['id'], 2)
        self.assertEqual(response_json['results'][1]['calculated_amount'], 25)

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
