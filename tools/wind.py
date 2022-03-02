_DIRECTION_DATA = (
    (348.75, "north"),
    (326.25, "north-northwest"),
    (303.75, "northwest"),
    (281.25, "west-northwest"),
    (258.75, "west"),
    (236.25, "west-southwest"),
    (213.75, "southwest"),
    (191.25, "south-southwest"),
    (168.75, "south"),
    (146.25, "south-southeast"),
    (123.75, "southeast"),
    (101.25, "east-southeast"),
    (78.75, "east"),
    (56.25, "east-northeast"),
    (33.75, "northeast"),
    (11.25, "north-northeast"),
    (0, "north"),
)
_DESCRIPTION_DATA = (
    (120, "Hurricane"),
    (103, "Violent storm"),
    (88, "Storm"),
    (76, "Severe gale"),
    (63, "Gale"),
    (51, "Near gale"),
    (40, "Strong breeze"),
    (30, "Fresh breeze"),
    (20, "Moderate breeze"),
    (12, "Gentle breeze"),
    (7, "Light breeze"),
    (1, "Light air"),
    (0, "Calm"),
)


def _ms_to_kmhr(speed):
    return speed * 3600 / 1000


def wind_degree_to_cardinal_direction(degree):
    if degree > 360 or degree < 0:
        return None

    for initial_degree, direction in _DIRECTION_DATA:
        if degree > initial_degree:
            return direction


def wind_speed_to_international_description(speed_in_ms):
    speed = _ms_to_kmhr(speed_in_ms)

    for km_hr, description in _DESCRIPTION_DATA:
        if speed >= km_hr:
            return description
