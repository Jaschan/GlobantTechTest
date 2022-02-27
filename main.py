from flask import Flask
from flask import request
from flask import abort
import weather_tools


app = Flask(__name__)


@app.route("/weather")
def weather():
    country = request.args.get('country', '').lower()
    if len(country) > 2:
        abort(422)
    city = request.args.get('city', '')
    output = weather_tools.get_weather_info(city, country)
    if output is None:
        abort(501)
    return output


# TODO: Delete this later
@app.route("/cache")
def cache():
    return str(weather_tools._cache)
