from flask import Flask
from flask import request
from flask import abort
import os
import requests
import datetime
import temperature_tools
import wind_tools


OPENWEATHERMAP_API_URL = os.getenv(
    'OPENWEATHERMAP_API_URL', 'http://api.openweathermap.org/data/2.5/weather')
OPENWEATHERMAP_APP_ID = os.getenv(
    'OPENWEATHERMAP_APP_ID', '1508a9a4840a5574c822d70ca2132032')

app = Flask(__name__)


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
    payload = {'q': place, 'appid': OPENWEATHERMAP_APP_ID}
    req = requests.get(OPENWEATHERMAP_API_URL, params=payload)
    if req.status_code == requests.codes.ok:
        return req.json()
    else:
        return {'cod': req.status_code}


def convert(owm_json):
    main = owm_json['main']
    sys = owm_json['sys']
    country = sys['country']

    location_name = "{city}, {country}".format(
        city=owm_json['name'],
        country=country)

    lat = owm_json['coord']['lat']
    lon = owm_json['coord']['lon']
    geo_coordinates = "[{lat:.2f}, {lon:.2f}]".format(lat=lat, lon=lon)

    temp_K = main['temp']
    temp_F = ''
    temp_C = ''
    if temp_K is not None:
        temp_F = temperature_tools.kelvin_to_fahrenheit(temp_K)
        temp_C = temperature_tools.kelvin_to_celsius(temp_K)
    temperature = "{celsius:.0f} °C, {fahrenheit:.0f} °F".format(
        celsius=temp_C,
        fahrenheit=temp_F)

    tz = datetime.timezone(
        datetime.timedelta(seconds=owm_json['timezone']))
    cloudiness = owm_json['weather'][0]['description'].capitalize()
    pressure = "{0} hpa".format(main['pressure'])
    humidity = "{0}%".format(main['humidity'])

    sunrise = datetime.datetime.fromtimestamp(
        sys['sunrise'], tz=tz).strftime("%H:%M")
    sunset = datetime.datetime.fromtimestamp(
        sys['sunset'], tz=tz).strftime("%H:%M")
    requested_time = datetime.datetime.fromtimestamp(
        owm_json['dt'], tz=tz).strftime("%Y-%m-%d %H:%M:%S")

    wind_speed = owm_json['wind']['speed']
    wind = "{description}, {speed} m/s, {direction}".format(
        description=wind_tools.wind_speed_to_international_description(
            wind_speed),
        speed=wind_speed,
        direction=wind_tools.wind_degree_to_cardinal_direction(

            owm_json['wind']['deg'])).capitalize()
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
