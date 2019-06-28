import math

from drf_extra_fields.geo_fields import PointField

from geopy.distance import vincenty


def computing_salary(to_address, from_address, to_location, from_location, weight):
    ''' function for computin salary '''

    FIXED_TAX = 0
    RATE = 0
    to_governate = to_address.split(",")[-2]
    from_governate = from_address.split(",")[-2]
    if isinstance(to_location, dict) and isinstance(to_location, dict):

        to_location = PointField().to_internal_value(to_location)
        from_location = PointField().to_internal_value(from_location)

    distance = vincenty(to_location.coords, from_location.coords).kilometers
    distance = math.ceil(distance)
    print(distance)

    if to_governate == from_governate:
        if weight < 5:
            RATE = 1.5
            FIXED_TAX = 5

        else:
            RATE = 1.60
            FIXED_TAX = 5 + ((weight-5))*0.5

    else:
        if weight < 20:
            RATE = 1.75
            FIXED_TAX = 20

        else:
            RATE = 2
            FIXED_TAX = 15

    return (round(distance*RATE+FIXED_TAX))
