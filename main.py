from flask import Flask
from flask import request
from flask import abort
import requests

app = Flask(__name__)

OPENWEATHERMAP_API = 'http://api.openweathermap.org/data/2.5/weather'
APP_ID = '1508a9a4840a5574c822d70ca2132032'

@app.route("/weather")
def weather():
  country = request.args.get('country', '').lower()
  if len(country) > 2 : abort(422)
  city = request.args.get('city', '')
  place = "{0},{1}".format(city, country)
  payload = {'q': place , 'appid': APP_ID}
  req = requests.get(OPENWEATHERMAP_API, params=payload)
  if req.status_code == requests.codes.ok:
    response = req.json()
    status_code = response.get('cod')
    if status_code != requests.codes.ok:
      abort(status_code)
    return response
  else:
    abort(req.status_code)

