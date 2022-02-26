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
    output = {
        "location_name": location_name,
        "temperature": temperature,
        "wind": "Gentle breeze, 3.6 m/s, west-northwest",
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
"""
{
"coord": {"lon": -74.0817,"lat":4.6097},
"weather":[{"id":803,"main":"Clouds","description":"broken clouds","icon":"04d"}],
"base":"stations",
"main":{"temp":288.88,"feels_like":288.39,"temp_min":288.88,"temp_max":288.88,"pressure":1023,"humidity":72},
"visibility":9000,
"wind":{"speed":4.63,"deg":180},
"clouds":{"all":75},
"dt":1645825284,
"sys":{"type":1,"id":8582,"country":"CO","sunrise":1645787347,"sunset":1645830600},
"timezone":-18000,
"id":3688689,
"name":"Bogota",
"cod":200
}
"""