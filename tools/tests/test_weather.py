import unittest
from unittest.mock import patch, MagicMock, Mock
import tools


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

    def test_get_weather_info(self):
        mocked_retrieve_from_cache = patch(
            'tools.weather._retrieve_from_cache',
            MagicMock(return_value=None)).start()
        mocked_call_external_api = patch(
            'tools.weather._call_external_api',
            MagicMock(return_value=self.json_from_openweathermap)).start()
        mocked_convert_to_required_layout = patch(
            'tools.weather._convert_to_required_layout',
            MagicMock(return_value=self.json_converted)).start()
        mocked_store_in_cache = patch(
            'tools.weather._store_in_cache',
            MagicMock(return_value=None)).start()

        cases = (
            ("bogota", "co"),
            ("tokyo", "jp"),
            ("osorno", "cl"),
        )
        for city, country in cases:
            with self.subTest(city=city, country=country):
                tools.weather.get_weather_info(city, country)
                mocked_retrieve_from_cache.assert_called_with((city, country))
                mocked_call_external_api.assert_called_with(city, country)
                mocked_convert_to_required_layout.assert_called_with(self.json_from_openweathermap)
                mocked_store_in_cache.assert_called_with((city, country), self.json_converted)
        mocked_retrieve_from_cache.stop()
        mocked_call_external_api.stop()
        mocked_convert_to_required_layout.stop()
        mocked_store_in_cache.stop()

    def test_call_external_api(self):
        self.maxDiff = None
        cases = (
            ("bogota", "co", 200, self.json_from_openweathermap),
            ("bogota", "co", 501, {'cod': 501}),
            ("bogota", "co", 200, {'cod': 501}),  # Looks weird, but it is possible
        )
        for city, country, status_code, response_json in cases:
            with self.subTest(city=city, country=country, status_code=status_code, response_json=response_json):
                mock = Mock()
                mock.json = Mock(return_value=response_json)
                mock.status_code = status_code
                with patch('requests.get', MagicMock(return_value=mock)) as patched:
                    response = tools.weather._call_external_api(city, country)
                    patched.assert_called_with(
                        tools.weather._OPENWEATHERMAP_API_URL,
                        params={'q': "{0},{1}".format(city, country),
                                'appid': tools.weather._OPENWEATHERMAP_APP_ID})
                    self.assertEqual(response, response_json)

    def test_json_convertion(self):
        self.assertEqual(
            tools.weather._convert_to_required_layout(self.json_from_openweathermap),
            self.json_converted)

    @patch('tools.weather.time', MagicMock(return_value=123.456789))
    def test_timestamp(self):
        self.assertEqual(tools.weather._timestamp(), 123456)
        assert tools.weather.time.called
