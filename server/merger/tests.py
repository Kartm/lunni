from io import StringIO, BytesIO

from mock import patch
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from django.test.client import MULTIPART_CONTENT, encode_multipart, BOUNDARY
from rest_framework.utils import json

from merger.factories import TransactionLogFactory
from merger.models import TransactionLog


class MergerTestCase(APITestCase):
    def test_upload_file(self):
        url = reverse('merger-upload')

        operations_file = """mBank S.A. Bankowość Detaliczna;
Skrytka Pocztowa 2108;
90-959 Łódź 2;
www.mBank.pl;
mLinia: 801 300 800;
+48 (42) 6 300 800;


#Klient;
ŁUKASZ BLACHNICKI;

Lista operacji;

#Za okres:;
XXXXXXX;

#zgodnie z wybranymi filtrami wyszukiwania;
#dla rachunków:;
Prywatne - XXXX;

#Lista nie jest dokumentem w rozumieniu art. 7 Ustawy Prawo Bankowe (Dz. U. Nr 140 z 1997 roku, poz.939 z późniejszymi zmianami), ponieważ operacje można samodzielnie edytować.;

#Waluta;#Wpływy;#Wydatki;
PLN;XXXXXXXXXX

#Data operacji;#Opis operacji;#Rachunek;#Kategoria;#Kwota;
2023-02-11;"Zwrot za maka";"Prywatne";"Wpływy";15,80 PLN;;
2023-02-10;"McDonalds";"Prywatne";"Jedzenie poza domem";-31,60 PLN;;
2023-02-10;"MPK Wrocław";"Prywatne";"Transport";-1,20 PLN;;
        """
        sio = StringIO(operations_file)
        bio = BytesIO(sio.read().encode('utf8'))

        response = self.client.post(
            path=url,
            data=encode_multipart(
                data=dict(file=bio),
                boundary=BOUNDARY,
            ),
            content_type=MULTIPART_CONTENT,
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        loaded_entries = json.loads(response.content)['loaded_rows']
        self.assertJSONEqual(
            json.dumps(loaded_entries),
            [
                {
                    'date': '2023-02-11',
                    'description': 'Zwrot za maka',
                    'account': 'Prywatne',
                    'category': 'Wpływy',
                    'amount': 1580
                },
                {
                    'date': '2023-02-10',
                    'description': 'McDonalds',
                    'account': 'Prywatne',
                    'category': 'Jedzenie poza domem',
                    'amount': -3160
                },
                {
                    'date': '2023-02-10',
                    'description': 'MPK Wrocław',
                    'account': 'Prywatne',
                    'category': 'Transport',
                    'amount': -120
                },
            ]
        )

        self.assertEqual(len(loaded_entries), 3)

    def test_get_transactions(self):
        transaction1 = TransactionLogFactory(
            id=1,
            amount=300
        )
        transaction2 = TransactionLogFactory(
            id=2,
            amount=-50
        )

        url = reverse('merger-merge')

        merge_body = {
            'from_transaction': 1,
            'to_transaction': 2,
            'amount': 49
        }

        response = self.client.post(
            path=url,
            data=json.dumps(merge_body),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = reverse('merger-transactions')

        response = self.client.get(
            path=url,
        )

        loaded_entries = json.loads(response.content)
        self.assertJSONEqual(
            json.dumps(loaded_entries),
            {
                'transactions': [
                    {
                        "id": 1,
                        "date": "2023-01-05",
                        "description": "desc",
                        "account": "prywatnte",
                        "category": "lol wydatkii",
                        "amount": 251
                    },
                    {
                        "id": 2,
                        "date": "2023-01-05",
                        "description": "desc",
                        "account": "prywatnte",
                        "category": "lol wydatkii",
                        "amount": -1
                    }
                ]
            }
        )
