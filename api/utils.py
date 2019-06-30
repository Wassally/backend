import math

from drf_extra_fields.geo_fields import PointField

from geopy.distance import vincenty

from rest_framework import serializers


def computing_salary(to_address, from_address, to_location, from_location, weight):
    ''' function for computin salary '''

    FIXED_TAX = 0
    try:
        to_governate = to_address.split(",")[-2]
        from_governate = from_address.split(",")[-2]
    except IndexError:
        raise serializers.ValidationError(
            {"massage": "pls give me a valid  governate with address"}
        )

    if isinstance(to_location, dict) and isinstance(to_location, dict):

        to_location = PointField().to_internal_value(to_location)
        from_location = PointField().to_internal_value(from_location)

    distance = vincenty(to_location.coords, from_location.coords).kilometers
    distance = math.ceil(distance)
    print(distance)

    if to_governate == from_governate:
        if weight < 5:
            FIXED_TAX = 25

        else:

            FIXED_TAX = 25 + ((weight-5))*0.5

    else:
        if weight < 5:

            FIXED_TAX = 65

        else:

            FIXED_TAX = 65 + ((weight-5))*0.5

    return (round(FIXED_TAX))
