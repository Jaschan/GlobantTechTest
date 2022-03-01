import unittest
from unittest.mock import patch, MagicMock, Mock
import weather_tools
import wind_tools
import temperature_tools


class TestCache(unittest.TestCase):
    @patch('weather_tools._timestamp', MagicMock(return_value=123456))
    def test_store_in_cache(self):
        key = ("city", "country")
        item = {"fake": "item"}
        weather_tools._store_in_cache(key, item)
        self.assertEqual(weather_tools._cache[key], (123456, item))
        assert weather_tools._timestamp.called

    @patch('weather_tools._timestamp', MagicMock(return_value=123456))
    def test_retrieve_from_cache(self):
        key = ("city", "country")
        item = {"fake": "item"}

        # Same time
        with patch.dict(weather_tools._cache, {key: (123456, item)}, clear=True):
            assert weather_tools._cache == {key: (123456, item)}
            self.assertEqual(weather_tools._retrieve_from_cache(key), item)
            assert weather_tools._timestamp.called
        assert weather_tools._cache == {}

        # Exactly 2 minutes
        with patch.dict(weather_tools._cache, {key: (123456 - 120, item)}, clear=True):
            assert weather_tools._cache == {key: (123456 - 120, item)}
            self.assertEqual(weather_tools._retrieve_from_cache(key), item)
            assert weather_tools._timestamp.called
        assert weather_tools._cache == {}

        # Exactly 2 minutes and 1 second
        with patch.dict(weather_tools._cache, {key: (123456 - 121, item)}, clear=True):
            assert weather_tools._cache == {key: (123456 - 121, item)}
            self.assertEqual(weather_tools._retrieve_from_cache(key), None)
            assert weather_tools._timestamp.called
        assert weather_tools._cache == {}

        # Very old cache
        with patch.dict(weather_tools._cache, {key: (1, item)}, clear=True):
            assert weather_tools._cache == {key: (1, item)}
            self.assertEqual(weather_tools._retrieve_from_cache(key), None)
            assert weather_tools._timestamp.called
        assert weather_tools._cache == {}

        # Future cache (should not happen, hence it should return None)
        with patch.dict(weather_tools._cache, {key: (float('inf'), item)}, clear=True):
            assert weather_tools._cache == {key: (float('inf'), item)}
            self.assertEqual(weather_tools._retrieve_from_cache(key), None)
            assert weather_tools._timestamp.called
        assert weather_tools._cache == {}


class TestWeatherTools(unittest.TestCase):
    def setUp(self):
        self.json_from_openweathermap = {
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
        self.json_converted = {
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

    # TODO: mock _call_external_api()
    def test_get_weather_info(self):
        #weather_tools.get_weather_info()
        pass

    def test_call_external_api(self):
        self.maxDiff = None
        cases = (
            ("osorno", "cl", 200, self.json_from_openweathermap),
            ("osorno", "cl", 501, {'cod': 501}),
            ("osorno", "cl", 200, {'cod': 501}),  # Looks weird, but it is possible
        )
        for city, country, status_code, response_json in cases:
            with self.subTest(city=city, country=country, status_code=status_code, response_json=response_json):
                mock = Mock()
                mock.json = Mock(return_value=response_json)
                mock.status_code = status_code
                with patch('requests.get', MagicMock(return_value=mock)) as patched:
                    response = weather_tools._call_external_api(city, country)
                    patched.assert_called_with(
                        weather_tools._OPENWEATHERMAP_API_URL,
                        params={'q': "{0},{1}".format(city, country),
                                'appid': weather_tools._OPENWEATHERMAP_APP_ID})
                    self.assertEqual(response, response_json)

    def test_json_convertion(self):
        self.assertEqual(
            weather_tools._convert_to_required_layout(self.json_from_openweathermap),
            self.json_converted)

    @patch('weather_tools.time', MagicMock(return_value=123.456789))
    def test_timestamp(self):
        self.assertEqual(weather_tools._timestamp(), 123456)
        assert weather_tools.time.called


class TestWindTools(unittest.TestCase):

    def test_wind_degree_to_cardinal_direction(self):
        test_data = (  # degree, cardinal direction
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
            with self.subTest(i=i, o=o):
                self.assertEqual(wind_tools.wind_degree_to_cardinal_direction(i), o)

    def test_wind_speed_to_international_description(self):
        test_data = (  # KM/H, Description
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
            with self.subTest(i=i, o=o):
                self.assertEqual(wind_tools.wind_speed_to_international_description(i), o)

    def test_ms_to_kmhr(self):
        self.assertAlmostEqual(wind_tools._ms_to_kmhr(0), 0)
        self.assertAlmostEqual(wind_tools._ms_to_kmhr(27.77777778), 100)
        self.assertAlmostEqual(wind_tools._ms_to_kmhr(10), 36)
        self.assertAlmostEqual(wind_tools._ms_to_kmhr(2), 7.2)


class TestTemperatureTools(unittest.TestCase):

    def setUp(self):
        self.data = (  # Kelvin, Celsius, Fahrenheit
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
            with self.subTest(k=k, c=c, f=f):
                self.assertAlmostEqual(temperature_tools.fahrenheit_to_celsius(f), c, delta=0.0001)

    def test_kelvin_to_celsius(self):
        for k, c, f in self.data:
            with self.subTest(k=k, c=c, f=f):
                self.assertAlmostEqual(temperature_tools.kelvin_to_celsius(k), c, delta=0.0001)

    def test_kelvin_to_fahrenheit(self):
        for k, c, f in self.data:
            with self.subTest(k=k, c=c, f=f):
                self.assertAlmostEqual(temperature_tools.kelvin_to_fahrenheit(k), f, delta=0.0001)


if __name__ == '__main__':
    unittest.main()
