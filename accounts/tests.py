import os

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

os.environ['DJANGO_SETTINGS_MODULE'] = 'todos.settings'


class AccountsTestCase(APITestCase):
    def test_register_is_working(self):
        url = reverse('accounts:register')
        body = {
            'username': 'test',
            'password': 'test-password1234',
        }
        response = self.client.post(url, body, format='json')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_login_is_working(self):
        url = reverse('accounts:login')
        body = {
            'username': 'test',
            'password': 'test-password1234',
        }
        response = self.client.post(url, body, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
