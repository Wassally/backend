from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from api.factories import ClientFactory, CaptainFactory


class AccountTest(APITestCase):
    '''Testing Account View'''

    def test_create_account_as_client(self):
        '''Testing Creating Account As Client'''

        data = {
            "username": "client",
            "email": "client@gmail.com",
            "password": "1",
            "is_client": True,
            "is_captain": False,
            "phone_number": 555,
        }

        response = self.client.post(
            reverse('accounts-list'),
            data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.json().get('is_client'))
        self.assertFalse(response.json().get('is_captain'))

    def test_create_account_as_captain(self):
        '''Testing Creating Account As Captain'''

        data = {
            "username": "captain",
            "email": "captain@gmail.com",
            "password": "1",
            "is_client": False,
            "is_captain": True,
            "phone_number": 555,
            "captain": {
                "national_id": "1111111111"
            }
        }

        response = self.client.post(
            reverse('accounts-list'),
            data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertFalse(response.json().get('is_client'))
        self.assertTrue(response.json().get('is_captain'))
