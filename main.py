from flask import Flask
from flask import request
from flask import abort
import tools


app = Flask(__name__)


@app.route("/weather")
def weather_api():
    country = request.args.get('country', '').lower()
    if len(country) > 2:
        abort(422)
    city = request.args.get('city', '')
    output = tools.weather.get_weather_info(city, country)
    if output is None:
        abort(501)
    return output
