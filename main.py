from flask import Flask
from flask import request
from flask import abort
import requests
import datetime


app = Flask(__name__)

OPENWEATHERMAP_API = 'http://api.openweathermap.org/data/2.5/weather'
APP_ID = '1508a9a4840a5574c822d70ca2132032'


@app.route("/weather")
def weather():
    country = request.args.get('country', '').lower()
    if len(country) > 2:
        abort(422)
    city = request.args.get('city', '')

    response = call_external_api(city, country)
    status_code = response.get('cod')

    if status_code != requests.codes.ok:
        abort(status_code)

    return convert(response)


def call_external_api(city, country):
    place = "{0},{1}".format(city, country)
    payload = {'q': place, 'appid': APP_ID}
    req = requests.get(OPENWEATHERMAP_API, params=payload)
    if req.status_code == requests.codes.ok:
        return req.json()
    else:
        return {'cod': req.status_code}


def fahrenheit_to_celsius(temperature):
    return (temperature - 32) * 5 / 9


def kelvin_to_celsius(temperature):
    return (temperature - 273.15)


def kelvin_to_fahrenheit(temperature):
    return (temperature - 273.15) * 9 / 5 + 32


def wind_degree_to_cardinal_direction(degree):
    if degree > 360 or degree < 0:
        return None
    direction_data = (
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
    for initial_degree, direction in direction_data:
        if degree > initial_degree:
            return direction


def ms_to_kmhr(speed):
    return speed * 3600 / 1000


def wind_speed_to_international_description(speed_in_ms):
    speed = ms_to_kmhr(speed_in_ms)
    description_data = (
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
    for km_hr, description in description_data:
        if speed >= km_hr:
            return description


def convert(owm_json):
    main = owm_json['main']
    sys = owm_json['sys']
    country = sys['country']
    tz = datetime.timezone(
        datetime.timedelta(seconds=owm_json['timezone']))

    location_name = "{city}, {country}".format(
        city=owm_json['name'],
        country=country)

    temp_K = main['temp']
    temp_F = ''
    temp_C = ''

    if temp_K is not None:
        temp_F = kelvin_to_fahrenheit(temp_K)
        temp_C = kelvin_to_celsius(temp_K)

    temperature = "{celsius:.0f} °C, {fahrenheit:.0f} °F".format(
        celsius=temp_C,
        fahrenheit=temp_F)

    cloudiness = owm_json['weather'][0]['description'].capitalize()
    pressure = "{0} hpa".format(main['pressure'])
    humidity = "{0}%".format(main['humidity'])
    lat = owm_json['coord']['lat']
    lon = owm_json['coord']['lon']
    geo_coordinates = "[{lat:.2f}, {lon:.2f}]".format(lat=lat, lon=lon)
    sunrise = datetime.datetime.fromtimestamp(
        sys['sunrise'], tz=tz).strftime("%H:%M")
    sunset = datetime.datetime.fromtimestamp(
        sys['sunset'], tz=tz).strftime("%H:%M")
    requested_time = datetime.datetime.fromtimestamp(
        owm_json['dt'], tz=tz).strftime("%Y-%m-%d %H:%M:%S")  # 2018-01-09 11:57:00
    wind_speed = owm_json['wind']['speed']
    wind = "{description}, {speed} m/s, {direction}".format(
        description=wind_speed_to_international_description(wind_speed),
        speed=wind_speed,
        direction=wind_degree_to_cardinal_direction(owm_json['wind']['deg'])
    ).capitalize()
    output = {
        "location_name": location_name,
        "temperature": temperature,
        "wind": wind,
        "cloudiness": cloudiness,
        "pressure": pressure,
        "humidity": humidity,
        "sunrise": sunrise,
        "sunset": sunset,
        "geo_coordinates": geo_coordinates,
        "requested_time": requested_time,
        "forecast": {}
    }
    return output
