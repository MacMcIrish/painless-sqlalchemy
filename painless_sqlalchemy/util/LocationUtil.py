from math import radians, cos, sin, asin, sqrt, isnan, isinf


def _validate_coordinate(coordinate, valid_range):
    """
        Check if a coordinate is valid. Throws error if not.
    :param coordinate: the input
    :param valid_range: the valid range (abs)
    :return: the coordinate
    """
    try:
        coordinate = float(coordinate)
    except (TypeError, ValueError) as err:
        raise ValueError('%s not a float' % str(coordinate), err)
    if isnan(coordinate) or isinf(coordinate):
        raise ValueError('%s can not be nan or inf' % str(coordinate))
    if abs(coordinate) > valid_range:
        raise ValueError(
            '%s is not in range %s' % (str(coordinate), str(valid_range)))
    return coordinate


def validate_latitude(latitude):
    """
        Check if latitude is valid.
    :param latitude: Latitude to check
    :return: the latitude if valid, otherwise throws error
    """
    try:
        return _validate_coordinate(latitude, 90)
    except Exception as e:
        raise ValueError("Invalid latitude given.", e)


def validate_longitude(longitude):
    """
        Check if longitude is valid.
    :param longitude: Longitude to check
    :return: the longitude if valid, otherwise throws error
    """
    try:
        return _validate_coordinate(longitude, 180)
    except Exception as e:
        raise ValueError("Invalid longitude given.", e)


def validate_latlong(latlong):
    """
        Check if latlong location is valid.

        Throws error if not
    :param latlong: Location to check
    :return: tuple (lat, long)
    """
    return validate_latitude(latlong[0]), validate_longitude(latlong[1])


def is_valid_latitude(latitude):
    """
        Check if latitude is valid
    :param latitude: Latitude to check
    :return: True iff latitude is valid
    """
    try:
        validate_latitude(latitude)
    except ValueError:
        return False
    return True


def is_valid_longitude(longitude):
    """
        Check if longitude is valid
    :param longitude: Longitude to check
    :return: True iff longitude is valid
    """
    try:
        validate_longitude(longitude)
    except ValueError:
        return False
    return True


def is_valid_latlong(latlong):
    """
        Check if latlong location is valid.
    :param latlong: Location to check
    :return: True iff valid tuple
    """
    return (
        len(latlong) == 2 and
        is_valid_latitude(latlong[0]) and
        is_valid_longitude(latlong[1])
    )


def is_valid_latlongrect(rect):
    """
        Check if four points form valid location rectangle.
    :param rect: Location rectangle to check
    :return: True iff valid tuple
    """
    return (
        len(rect) == 4 and
        is_valid_latitude(rect[0]) and
        is_valid_longitude(rect[1]) and
        is_valid_latitude(rect[2]) and
        is_valid_longitude(rect[3]) and
        validate_latitude(rect[0]) < validate_latitude(rect[2]) and
        validate_longitude(rect[1]) < validate_longitude(rect[3])
    )


def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees).
    Returns distance in km.

    Important: Result is an approximation
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371
    return c * r


def point_inside_polygon(x, y, poly):
    """
    Determine if a point is inside a given polygon or not.
    Polygon is a list of (x,y) pairs.

    If the test point is on the border of the polygon, this algorithm
    will deliver unpredictable results.

    If the polygon is overlapping this algorithm will not work reliably.

    Example:
    x, y = 1, 1
    poly = [(0,0), (2,0), (2,2), (0,2), (0,0)]

    Source: http://tiny.cc/rfkp4x
    """
    assert poly[0][0] == poly[-1][0] and poly[0][1] == poly[-1][1]

    n = len(poly)
    inside = False

    p1x, p1y = poly[0]
    for i in range(1, n):
        p2x, p2y = poly[i]
        # Note: The first check prevents p2y == p1y (division by zero)
        if (
            (p1y > y) != (p2y > y) and
            x < (p2x - p1x) * (y - p1y) / (p2y - p1y) + p1x
        ):
            inside = not inside
        p1x, p1y = p2x, p2y

    return inside
