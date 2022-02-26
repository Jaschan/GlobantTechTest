import unittest
from main import fahrenheit_to_celsius, kelvin_to_celsius, kelvin_to_fahrenheit
from main import call_external_api, convert, ms_to_kmhr
from main import wind_degree_to_cardinal_direction, wind_speed_to_international_description


class TestOpenWeatherMapAPI(unittest.TestCase):

    def test_call_external_api(self):
        response = call_external_api("osorno", "cl")
        self.assertEqual(response['cod'], 200)

    def test_json_convertion(self):
        dummy = {
            "coord": {"lon": -74.0817, "lat": 4.6097},
            "weather": [
                {
                    "id": 803,
                    "main": "Clouds",
                    "description": "scattered clouds",
                    "icon": "04d"
                }
            ],
            "base": "stations",
            "main": {
                "temp": 290.15,
                "feels_like": 288.39,
                "temp_min": 288.88,
                "temp_max": 288.88,
                "pressure": 1027,
                "humidity": 63
            },
            "visibility": 9000,
            "wind": {"speed": 3.6, "deg": 180},
            "clouds": {"all": 75},
            "dt": 1645825284,
            "sys": {
                "type": 1,
                "id": 8582,
                "country": "CO",
                "sunrise": 1645787347,
                "sunset": 1645830600
            },
            "timezone": -18000,
            "id": 3688689,
            "name": "Bogota",
            "cod": 200
        }
        correct_answer = {
            "location_name": "Bogota, CO",
            "temperature": "17 °C, 63 °F",
            "wind": "Gentle breeze, 3.6 m/s, south",
            "cloudiness": "Scattered clouds",
            "pressure": "1027 hpa",
            "humidity": "63%",
            "sunrise": "06:09",
            "sunset": "18:10",
            "geo_coordinates": "[4.61, -74.08]",
            "requested_time": "2022-02-25 16:41:24",
            "forecast": {}
        }

        self.assertEqual(convert(dummy), correct_answer)

    def test_wind_degree_to_cardinal_direction(self):
        test_data = (
            (348.76, "north"),
            (11.24, "north"),
            (11.26, "north-northeast"),
            (33.74, "north-northeast"),
            (33.76, "northeast"),
            (56.24, "northeast"),
            (56.26, "east-northeast"),
            (78.74, "east-northeast"),
            (78.76, "east"),
            (101.24, "east"),
            (101.26, "east-southeast"),
            (123.74, "east-southeast"),
            (123.76, "southeast"),
            (146.24, "southeast"),
            (146.26, "south-southeast"),
            (168.74, "south-southeast"),
            (168.76, "south"),
            (191.24, "south"),
            (191.26, "south-southwest"),
            (213.74, "south-southwest"),
            (213.76, "southwest"),
            (236.24, "southwest"),
            (236.26, "west-southwest"),
            (258.74, "west-southwest"),
            (258.76, "west"),
            (281.24, "west"),
            (281.26, "west-northwest"),
            (303.74, "west-northwest"),
            (303.76, "northwest"),
            (326.24, "northwest"),
            (326.26, "north-northwest"),
            (348.74, "north-northwest"),
        )
        for i, o in test_data:
            self.assertEqual(wind_degree_to_cardinal_direction(i), o)

    def test_wind_speed_to_international_description(self):
        test_data = (
            (0, "Calm"),
            (0.26, "Calm"),
            (0.28, "Light air"),
            (1.67, "Light air"),
            (1.95, "Light breeze"),
            (3.06, "Light breeze"),
            (3.34, "Gentle breeze"),
            (5.28, "Gentle breeze"),
            (5.56, "Moderate breeze"),
            (8.06, "Moderate breeze"),
            (8.34, "Fresh breeze"),
            (10.83, "Fresh breeze"),
            (11.12, "Strong breeze"),
            (13.89, "Strong breeze"),
            (14.17, "Near gale"),
            (17.22, "Near gale"),
            (17.50, "Gale"),
            (20.83, "Gale"),
            (21.12, "Severe gale"),
            (24.17, "Severe gale"),
            (24.45, "Storm"),
            (28.33, "Storm"),
            (28.62, "Violent storm"),
            (33.06, "Violent storm"),
            (33.34, "Hurricane"),
            (100, "Hurricane"),
        )
        for i, o in test_data:
            self.assertEqual(wind_speed_to_international_description(i), o)

    def test_ms_to_kmhr(self):
        self.assertAlmostEqual(ms_to_kmhr(0), 0)
        self.assertAlmostEqual(ms_to_kmhr(27.77777778), 100)
        self.assertAlmostEqual(ms_to_kmhr(10), 36)
        self.assertAlmostEqual(ms_to_kmhr(2), 7.2)


class TestTemperatureConvertion(unittest.TestCase):
    data = (  # Kelvin, Celsius, Fahrenheit
        (0, -273.15, -459.67),
        (1, -272.15, -457.87),
        (2, -271.15, -456.07),
        (4, -269.15, -452.47),
        (8, -265.15, -445.27),
        (16, -257.15, -430.87),
        (32, -241.15, -402.07),
        (64, -209.15, -344.47),
        (100, -173.15, -279.67),
        (128, -145.15, -229.27),
        (256, -17.15, 1.13),
        (512, 238.85, 461.93),
        (1024, 750.85, 1383.53),
        (2048, 1774.85, 3226.73),
        (10, -263.15, -441.67),
        (100, -173.15, -279.67),
        (200, -73.15, -99.67),
        (300, 26.85, 80.33),
        (400, 126.85, 260.33),
        (500, 226.85, 440.33),
        (600, 326.85, 620.33),
        (1000, 726.85, 1340.33),
        (233.15, -40, -40),
        (255.3722, -17.777777777, 0),
        (260.9278, -12.2222, 10.00004),
        (266.4833, -6.6667, 19.99994),
        (283.15, 10, 50),
        (270.95, -2.2, 28.04),
        (273.15, 0, 32),
        (373.15, 100, 212),
        (274.15, 1, 33.8),
        (293.15, 20, 68),
        (308.15, 35, 95),
        (315.15, 42, 107.6),
        (1.123456789, -272.02654321, -457.64777778),
        (-273.15, -546.3, -951.34),
    )

    def test_temperature_convertion(self):
        for k, c, f in self.data:
            self.assertAlmostEqual(fahrenheit_to_celsius(f), c, delta=0.0001)

    def test_kelvin_to_celsius(self):
        for k, c, f in self.data:
            self.assertAlmostEqual(kelvin_to_celsius(k), c, delta=0.0001)

    def test_kelvin_to_fahrenheit(self):
        for k, c, f in self.data:
            self.assertAlmostEqual(kelvin_to_fahrenheit(k), f, delta=0.0001)


if __name__ == '__main__':
    unittest.main()
