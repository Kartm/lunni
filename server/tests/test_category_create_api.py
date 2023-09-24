from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TestCategoryCreateAPI(APITestCase):
    def test_create_valid_category(self):
        url = reverse('categories')

        response = self.client.post(path=url, data={'name': 'Income', 'variant': 'POS'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_reject_invalid_category(self):
        url = reverse('categories')

        response = self.client.post(path=url, data={'name': 'None', 'variant': 'POS'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
