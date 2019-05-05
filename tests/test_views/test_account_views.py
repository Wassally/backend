from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from faker import Faker
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

    def test_retrieve_all_accounts(self):
        '''Retriving all Accounts'''

        client = ClientFactory()
        token = Token.objects.create(user=client)
        captain = CaptainFactory()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get(reverse('accounts-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_modify_accounts_as_owner(self):
        ''' Patch request testing from the owner of the account '''
        user = get_user_model()
        fake = Faker()
        client = ClientFactory()
        token = Token.objects.create(user=client)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        data = {
            "username": "test11",
            "email": fake.email(),
            "password": "55",
            "city": Faker('ar_EG').city(),
            "governate": Faker('ar_EG').country(),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "is_client": False,
            "is_captain": True
        }
        response = self.client.patch(
            reverse('accounts-detail', kwargs={"pk": client.id}),
            data=data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.json().get('is_client'))
        self.assertFalse(response.json().get('is_captain'))
        self.assertEqual(response.json().get('username'), data.get('username'))
        self.assertEqual(response.json().get('email'), data.get('email'))
        self.assertEqual(response.json().get('first_name'),
                         data.get('first_name'))
        self.assertEqual(response.json().get('city'), data.get('city'))
        self.assertEqual(response.json().get('governate'),
                         data.get('governate'))
        # i will check for password put it will need some research
