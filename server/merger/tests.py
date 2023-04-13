from io import StringIO, BytesIO

from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from django.test.client import MULTIPART_CONTENT, encode_multipart, BOUNDARY
from rest_framework.utils import json

from merger.factories import TransactionLogFactory, TransactionCategoryFactory, TransactionCategoryMatcherFactory


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
        self.assertJSONEqual(response.content, {})

    def test_get_transactions(self):
        TransactionLogFactory(
            id=1,
            amount=300
        )
        TransactionLogFactory(
            id=2,
            amount=-50
        )

        url = reverse('merger-transactions')

        response = self.client.get(
            path=url,
        )

        self.assertJSONEqual(
            response.content,
            {
                'count': 2,
                'total_pages': 1,
                'results': [
                    {
                        "id": 2,
                        "date": "2023-01-05",
                        "description": "desc",
                        "account": "prywatnte",
                        "category": {
                            'id': 2,
                            'name': 'food',
                            'variant': 'NEG'
                        },
                        "amount": -50
                    },
                    {
                        "id": 1,
                        "date": "2023-01-05",
                        "description": "desc",
                        "account": "prywatnte",
                        "category": {
                            'id': 1,
                            'name': 'food',
                            'variant': 'NEG'
                        },
                        "amount": 300
                    }
                ]
            }
        )

    def test_merge_transactions(self):
        TransactionLogFactory(
            id=1,
            amount=300
        )
        TransactionLogFactory(
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

        self.assertJSONEqual(
            response.content,
            {
                'count': 2,
                'total_pages': 1,
                'results': [
                    {
                        "id": 2,
                        "date": "2023-01-05",
                        "description": "desc",
                        "account": "prywatnte",
                        "category": {
                            'id': 2,
                            'name': 'food',
                            'variant': 'NEG'
                        },
                        "amount": -1
                    },
                    {
                        "id": 1,
                        "date": "2023-01-05",
                        "description": "desc",
                        "account": "prywatnte",
                        "category": {
                            'id': 1,
                            'name': 'food',
                            'variant': 'NEG'
                        },
                        "amount": 251
                    }
                ]
            }
        )

    def test_rematch_categories(self):
        TransactionLogFactory(
            id=1,
            amount=300,
            description='gift',
            category=None
        )
        TransactionLogFactory(
            id=2,
            amount=-50,
            description='spotify payment',
            category=None
        )
        subscriptionsCategory = TransactionCategoryFactory(
            id=1,
            name='subscriptions',
            variant='NEG'
        )
        TransactionCategoryMatcherFactory(
            id=1,
            regex_expression='spotify',
            category=subscriptionsCategory
        )

        url = reverse('rematch-categories')

        response = self.client.post(
            path=url,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('merger-transactions')

        response = self.client.get(
            path=url,
        )

        self.assertJSONEqual(
            response.content,
            {
                'count': 2,
                'total_pages': 1,
                'results': [
                    {
                        "id": 2,
                        "date": "2023-01-05",
                        "description": "spotify payment",
                        "account": "prywatnte",
                        "category": {
                            'id': 1,
                            'name': 'subscriptions',
                            'variant': 'NEG'
                        },
                        "amount": -50
                    },
                    {
                        "id": 1,
                        "date": "2023-01-05",
                        "description": "gift",
                        "account": "prywatnte",
                        "category": None,
                        "amount": 300
                    }
                ]
            }
        )
