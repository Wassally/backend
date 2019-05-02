from django.test import TestCase
from api.factories import ClientFactory
from api.models import User


class UserTest(TestCase):

    def test_creation_client(self):
        client = ClientFactory()

        self.assertTrue(isinstance(client, User))
        self.assertEqual(
            client.__str__(),
            "%d: %s" % (client.id, client.username)
        )
