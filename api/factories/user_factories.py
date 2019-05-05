import os
import factory
from ..models import User, Captain
from wassally.settings import MEDIA_ROOT
import faker


class ClientFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    image = factory.django.ImageField(
        from_path=os.path.join(MEDIA_ROOT, "default.png"),
        format="png"
    )
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    username = factory.LazyAttribute(
        lambda a: '{0}_{1}'.format(a.first_name, a.last_name)
    )
    email = factory.LazyAttribute(
        lambda a: '{0}.{1}@example.com'.format(a.first_name, a.last_name)
    )
    is_client = True
    is_captain = False
    governate = faker.Faker('ar_EG').country()
    city = faker.Faker('ar_EG').city()
    phone_number = factory.Sequence(lambda n: "0101176018{}".format(n))
    password = 1


class UserCaptainFactory(ClientFactory):

    is_captain = True
    is_client = False


class CaptainFactory(factory.DjangoModelFactory):
    class Meta:
        model = Captain
    national_id = factory.Sequence(lambda n: '1111111{}'.format(n))
    vehicle = "car"
    user = factory.SubFactory(UserCaptainFactory)
