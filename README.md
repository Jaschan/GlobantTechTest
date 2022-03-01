# GlobantTechTest

Goal: Create a Weather API.

## Instructions to run the code

### Windows PowerShell

This steps assumes that **git**, **python** and **pip** are installed

```
git clone https://github.com/Jaschan/GlobantTechTest.git
cd GlobantTechTest
python -m venv venv
Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope CurrentUser
# Select 'S'
.\venv\Scripts\Activate.ps1
pip install -r .\requirements.txt
$env:FLASK_APP = "main"
python -m flask run
```

Optional config examples

```
$env:FLASK_RUN_HOST = 'localhost'
$env:FLASK_RUN_HOST = '192.168.0.2'
$env:FLASK_RUN_PORT = 8000
$env:OPENWEATHERMAP_API_URL = 'http://api.openweathermap.org/data/2.5/weather'
$env:OPENWEATHERMAP_APP_ID = '1508a9a4840a5574c822d70ca2132032'
```


## Requirements

- [x] Commit your changes to a public repository in Github.
- [x] Add a README.md with instructions to run the code
- [x] Support the following endpoints
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
- [x] The data must be human-readable
- [x] Deliver both Temperatures in Celsius and Fahrenheit
- [x] Use environment variables for configuration
- [x] The response must include the content-type header (application/json)
- [x] Functions must be tested
- [X] Keep a cache of 2 minutes of the data. You can use a persistence layer for this.

## Resources

- Open Weather Map API Documentation https://openweathermap.org/current
- Wind direction and degrees http://snowfence.umn.edu/Components/winddirectionanddegrees.htm
- Classification of wind speeds https://nesa.cap.gov/media/cms/Beaufort_Wind_Scale_Chart_9697766BC_FAA31559D462A.pdf