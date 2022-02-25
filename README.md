# GlobantTechTest

Goal: Create a Weather API.

## Instructions to run the code

### Windows PowerShell

This steps asumes that **git**, **python** and **pip** are installed

```
git clone https://github.com/Jaschan/GlobantTechTest.git
cd GlobantTechTest
pip install -r .\requirements.txt
$env:FLASK_APP = "main"
flask run
```

## Requirements

- [x] Commit your changes to a public repository in Github.
- [x] Add a README.md with instructions to run the code
- [ ] Support the following endpoints
  > GET /weather?city=$City&country=$Country&
  ```
  Response: {
	  "location_name": "Bogota, CO",
	  "temperature": "17 °C",
	  "wind": Gentle breeze, 3.6 m/s, west-northwest",
	  "cloudiness": "Scattered clouds",
	  "pressure": "1027 hpa",
	  "humidity": "63%",
	  "sunrise": "06:07",
	  "sunset": "18:00",
	  "geo_coordinates": "[4.61, -74.08]",
	  "requested_time": "2018-01-09 11:57:00"
	  "forecast": {...}
  }
  ```
- [x] City is a string. Example: Valledupar
- [x] Country is a country code of two characters in lowercase. Example: co
- [x] This endpoint should use an external API to get the proper info, here is an example: http://api.openweathermap.org/data/2.5/weather?q=Bogota,co&appid=1508a9a4840a5574c822d70ca2132032
- [ ] The data must be human-readable
- [ ] Deliver both Temperatures in Celsius and Fahrenheit
- [ ] Use environment variables for configuration
- [x] The response must include the content-type header (application/json)
- [ ] Functions must be tested
- [ ] Keep a cache of 2 minutes of the data. You can use a persistence layer for this.
