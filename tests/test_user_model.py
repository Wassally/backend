from django.test import TestCase
from api.factories import ClientFactory, CaptainFactory
from api.models import User, Captain


class ClientTest(TestCase):

    def test_creation_client(self):
        client = ClientFactory()

        self.assertTrue(isinstance(client, User))
        self.assertEqual(
            client.__str__(),
            "%d: %s" % (client.id, client.username)
        )
        self.assertTrue(client.is_client)
        self.assertFalse(client.is_captain)


class CaptainTest(TestCase):

    def test_creation_captain(self):
        captain = CaptainFactory()

        self.assertTrue(isinstance(captain, Captain))
        self.assertEqual(captain.__str__(), captain.user.username)
        self.assertTrue(captain.user.is_captain)
        self.assertFalse(captain.user.is_client)
