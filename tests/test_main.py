import unittest
from unittest.mock import patch, MagicMock
import main


class TestMain(unittest.TestCase):
    def setUp(self):
        self.mock_exception = MagicMock(set=Exception)

        def abort(error_code):
            raise self.mock_exception(error_code)

        self.mocked_abort = patch(
            'main.abort', MagicMock(side_effect=abort)).start()
        self.mocked_request = patch('main.request', MagicMock()).start()

    def tearDown(self):
        self.mocked_abort.stop()
        self.mocked_request.stop()

    def test_weather_api(self):
        json_converted = {
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
        with patch('main.tools.weather.get_weather_info', MagicMock(return_value=json_converted)):
            self.mocked_request.args = {'country': 'co', 'city': 'bogota'}
            self.assertEqual(main.weather_api(), json_converted)

    @patch('main.tools.weather.get_weather_info', MagicMock(return_value=None))
    def test_weather_api_error_code_422(self):
        self.mocked_request.args = {'country': 'colombia', 'city': 'bogota'}
        with self.assertRaises(Exception):
            main.weather_api()
        self.mock_exception.assert_called_with(422)

    @patch('main.tools.weather.get_weather_info', MagicMock(return_value=None))
    def test_weather_api_error_code_501(self):
        self.mocked_request.args = {'country': 'co', 'city': 'bogota'}
        with self.assertRaises(Exception):
            main.weather_api()
        self.mock_exception.assert_called_with(501)
