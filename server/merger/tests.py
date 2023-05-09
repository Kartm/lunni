from io import StringIO, BytesIO

from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from django.test.client import MULTIPART_CONTENT, encode_multipart, BOUNDARY
from rest_framework.utils import json

from merger.factories import TransactionLogFactory, TransactionCategoryFactory, TransactionCategoryMatcherFactory


class MergerTestCase(APITestCase):
    def test_upload_mbank_file(self):
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
2023-02-11;"Zwrot za Maka";"Prywatne";"Wpływy";15,80 PLN;;
2023-02-10;"Stacja Grawitacja Cz-wa  ZAKUP PRZY UŻYCIU KARTY W KRAJU                                                     transakcja nierozliczona";"Prywatne";"Jedzenie poza domem";-31,60 PLN;;
        """
        sio = StringIO(operations_file)
        bio = BytesIO(sio.read().encode('utf8'))

        response = self.client.post(
            path=url,
            data=encode_multipart(
                data=dict(file=bio, variant='mbank'),
                boundary=BOUNDARY,
            ),
            content_type=MULTIPART_CONTENT,
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_content = response.json()['new_entries']
        self.assertEqual(len(response_content), 2)

        first_entry = response_content[0]
        self.assertEqual(first_entry['date'], '2023-02-11')
        self.assertEqual(first_entry['description'], 'Zwrot za Maka')
        self.assertEqual(first_entry['account'], 'Prywatne')
        self.assertIsNone(first_entry.get('category'))
        self.assertEqual(first_entry['amount'], 1580)

        second_entry = response_content[1]
        self.assertEqual(second_entry['date'], '2023-02-10')
        self.assertEqual(second_entry['description'],
                         'Stacja Grawitacja Cz-wa ZAKUP PRZY UŻYCIU KARTY W KRAJU transakcja nierozliczona')
        self.assertEqual(second_entry['account'], 'Prywatne')
        self.assertIsNone(second_entry.get('category'))
        self.assertEqual(second_entry['amount'], -3160)

    def test_prevent_duplicates(self):
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
2023-02-11;"Zwrot za Maka";"Prywatne";"Wpływy";15,80 PLN;;
2023-02-10;"Stacja Grawitacja Cz-wa  ZAKUP PRZY UŻYCIU KARTY W KRAJU                                                     transakcja nierozliczona";"Prywatne";"Jedzenie poza domem";-31,60 PLN;;
2023-02-10;"Stacja Grawitacja Cz-wa  ZAKUP PRZY UŻYCIU KARTY W KRAJU                                                     transakcja nierozliczona";"Prywatne";"Jedzenie poza domem";-31,60 PLN;;
        """
        sio = StringIO(operations_file)
        bio = BytesIO(sio.read().encode('utf8'))

        response = self.client.post(
            path=url,
            data=encode_multipart(
                data=dict(file=bio, variant='mbank'),
                boundary=BOUNDARY,
            ),
            content_type=MULTIPART_CONTENT,
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_content = response.json()['new_entries']
        self.assertEqual(len(response_content), 2)

        sio = StringIO(operations_file)
        bio = BytesIO(sio.read().encode('utf8'))

        response = self.client.post(
            path=url,
            data=encode_multipart(
                data=dict(file=bio, variant='mbank'),
                boundary=BOUNDARY,
            ),
            content_type=MULTIPART_CONTENT,
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_content = response.json()['new_entries']
        self.assertEqual(len(response_content), 0)

    def test_upload_pko_file(self):
        url = reverse('merger-upload')

        operations_file = """
"Data operacji","Data waluty","Typ transakcji","Kwota","Waluta","Saldo po transakcji","Opis transakcji","","","",""
"2023-05-08","2023-05-08","Przelew na rachunek","+20.70","PLN","+23.99","Costam","Nazwa nadawcy: BIURO","Adres nadawcyxxxx","",""
"2023-05-08","2023-05-08","Przelew na rachunek","+20.70","PLN","+23.99","Rachunek nadawcy: XXXX","Nazwa nadawcy: BIURO","Adres nadawcyxxxx","Tytul: sddsd",""
        """
        sio = StringIO(operations_file)
        bio = BytesIO(sio.read().encode('utf8'))

        response = self.client.post(
            path=url,
            data=encode_multipart(
                data=dict(file=bio, variant='pko'),
                boundary=BOUNDARY,
            ),
            content_type=MULTIPART_CONTENT,
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_content = response.json()['new_entries']
        self.assertEqual(len(response_content), 2)

        first_entry = response_content[0]
        self.assertEqual(first_entry['date'], '2023-05-08')
        self.assertEqual(first_entry['description'], 'Costam')
        self.assertEqual(first_entry['account'], 'PKO')
        self.assertIsNone(first_entry.get('category'))
        self.assertEqual(first_entry['amount'], 2070)

        second_entry = response_content[1]
        self.assertEqual(second_entry['date'], '2023-05-08')
        self.assertEqual(second_entry['description'], 'Tytul: sddsd')
        self.assertEqual(second_entry['account'], 'PKO')
        self.assertIsNone(second_entry.get('category'))
        self.assertEqual(second_entry['amount'], 2070)

    def test_get_transactions(self):
        TransactionLogFactory.create(id=1, amount=300)
        TransactionLogFactory.create(id=2, amount=-50)

        url = reverse('merger-transactions')

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
        self.assertEqual(first_result['category']['id'], 2)
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
        TransactionLogFactory(id=1, amount=300)
        TransactionLogFactory(id=2, amount=-50)
        TransactionLogFactory(id=3, amount=100)
        TransactionLogFactory(id=4, amount=-100)

        url = reverse('merger-merge')

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

        url = reverse('merger-transactions')

        response_json = self.client.get(path=url).json()

        self.assertEqual(response_json['count'], 2)
        self.assertEqual(response_json['total_pages'], 1)
        self.assertEqual(response_json['results'][0]['id'], 2)
        self.assertEqual(response_json['results'][0]['calculated_amount'], -1)
        self.assertEqual(response_json['results'][1]['id'], 1)
        self.assertEqual(response_json['results'][1]['calculated_amount'], 251)

    def test_merge_transactions_prevent_negative_amount(self):
        TransactionLogFactory(id=1, amount=300)
        TransactionLogFactory(id=2, amount=-50)

        url = reverse('merger-merge')

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
        TransactionLogFactory(id=1, amount=300)
        TransactionLogFactory(id=2, amount=-50)

        url = reverse('merger-merge')

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
        TransactionLogFactory(id=1, amount=300)
        TransactionLogFactory(id=2, amount=-50)

        url = reverse('merger-merge')

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

    def test_merge_multiple_transactions(self):
        TransactionLogFactory(id=1, amount=-75)
        TransactionLogFactory(id=2, amount=50)
        TransactionLogFactory(id=3, amount=25)

        url = reverse('merger-merge')

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

        url = reverse('merger-transactions')

        response_json = self.client.get(path=url).json()

        self.assertEqual(response_json['count'], 2)
        self.assertEqual(response_json['total_pages'], 1)
        self.assertEqual(response_json['results'][0]['id'], 1)
        self.assertEqual(response_json['results'][0]['calculated_amount'], -25)
        self.assertEqual(response_json['results'][1]['id'], 2)
        self.assertEqual(response_json['results'][1]['calculated_amount'], 25)

        # todo add choosing merge direction and validate existing ones
        # todo django admin uses model manager and hides objects with calculated amount = 0

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
