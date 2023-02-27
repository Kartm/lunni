from rest_framework.test import APITestCase
from django.urls import reverse
import os.path
from django.test.client import MULTIPART_CONTENT, encode_multipart, BOUNDARY


class FilesTestCase(APITestCase):
    def test_upload_file(self):
        url = reverse('files-home')
        with open(os.path.dirname(__file__) + '/../operations.csv', 'rb') as file:
            response = self.client.post(
                path=url,
                data=encode_multipart(
                    data=dict(file=file),
                    boundary=BOUNDARY,
                ),
                content_type=MULTIPART_CONTENT,
            )

            assert response.status_code == 200
