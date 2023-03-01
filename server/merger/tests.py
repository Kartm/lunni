from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
import os.path
from django.test.client import MULTIPART_CONTENT, encode_multipart, BOUNDARY
from rest_framework.utils import json


class MergerTestCase(APITestCase):
    def test_upload_file(self):
        url = reverse('merger-home')
        with open(os.path.dirname(__file__) + '/../operations.csv', 'rb') as file:
            response = self.client.post(
                path=url,
                data=encode_multipart(
                    data=dict(file=file),
                    boundary=BOUNDARY,
                ),
                content_type=MULTIPART_CONTENT,
            )

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

            loaded_entries = json.loads(response.content)['loaded_rows']
            response_first_entry = loaded_entries[0]
            self.assertJSONEqual(
                json.dumps(response_first_entry),
                {
                    'date': '2023-02-10',
                    'description': 'McDonalds 61600265  ZAKUP PRZY UŻYCIU KARTY - INTERNET                                                  transakcja nierozliczona',
                    'account': 'Prywatne 8811 ... 3099',
                    'category': 'Jedzenie poza domem',
                    'amount': -31.6
                }
            )

            self.assertEqual(len(loaded_entries), 1394)
