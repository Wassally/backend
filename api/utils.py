import math

from drf_extra_fields.geo_fields import PointField

from geopy.distance import vincenty


def computing_salary(to_location, from_location, weight):
    ''' function for computin salary '''

    FIXED_TAX = 0
    RATE = 0
    if isinstance(to_location, dict) and isinstance(to_location, dict):

        to_location = PointField().to_internal_value(to_location)
        from_location = PointField().to_internal_value(from_location)

    distance = vincenty(to_location.coords, from_location.coords).kilometers
    distance = math.ceil(distance)
    if weight < 5:
        RATE = 1.5
        FIXED_TAX = 5
        return (RATE*distance+FIXED_TAX)
    else:
        RATE = 1.5
        FIXED_TAX = 5 + ((weight-5))*0.5
        return (RATE*distance+FIXED_TAX)
