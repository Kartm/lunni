import os
from io import BytesIO

from django.test.client import MULTIPART_CONTENT, encode_multipart, BOUNDARY
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.utils import json

from api.factories import TransactionFactory, CategoryFactory


class TestTransactionUploadAPI(APITestCase):
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
        with open(os.path.join(os.path.dirname(__file__), os.pardir, 'tests/resources', 'mbank_statement_file.csv'),
                  mode='rb') as f:
            bio = BytesIO(f.read())
            response = self.upload_file(bio, 'mbank')

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            response_content = response.json()['new_entries']
            self.assertEqual(response_content, 2)

    def test_upload_mbank_savings_file(self):
        with open(os.path.join(os.path.dirname(__file__), os.pardir, 'tests/resources', 'mbank_statement_savings_file.csv'),
                  mode='rb') as f:
            bio = BytesIO(f.read())
            response = self.upload_file(bio, 'mbank-savings')

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            response_content = response.json()['new_entries']
            self.assertEqual(response_content, 2)

    def test_prevent_csv_duplicates(self):
        with open(os.path.join(os.path.dirname(__file__), os.pardir, 'tests/resources', 'mbank_statement_duplicate_file.csv'),
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

        with open(os.path.join(os.path.dirname(__file__), os.pardir, 'tests/resources', 'mbank_statement_database_duplicate_file.csv'),
                  mode='rb') as f:
            bio = BytesIO(f.read())
            response = self.upload_file(bio, 'mbank')

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            response_content = response.json()['new_entries']
            self.assertEqual(response_content, 0)

    def test_upload_pko_file(self):
        with open(os.path.join(os.path.dirname(__file__), os.pardir, 'tests/resources', 'pko_statement_file.csv'),
                  mode='rb') as f:
            bio = BytesIO(f.read())
            response = self.upload_file(bio, 'pko')

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            response_content = response.json()['new_entries']
            self.assertEqual(response_content, 2)

    def test_upload_ing_file(self):
        with open(os.path.join(os.path.dirname(__file__), os.pardir, 'tests/resources', 'ing_statement_file.csv'),
                  mode='rb') as f:
            bio = BytesIO(f.read())
            response = self.upload_file(bio, 'ing')

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            response_content = response.json()['new_entries']
            self.assertEqual(response_content, 3)

    def test_upload_file_compare_by_amount(self):
        with open(os.path.join(os.path.dirname(__file__), os.pardir, 'tests/resources', 'mbank_statement_file.csv'),
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
