import unittest
from unittest.mock import patch, MagicMock, Mock
import tools


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
                self.assertEqual(tools.wind.wind_degree_to_cardinal_direction(i), o)

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
                self.assertEqual(tools.wind.wind_speed_to_international_description(i), o)

    def test_ms_to_kmhr(self):
        self.assertAlmostEqual(tools.wind._ms_to_kmhr(0), 0)
        self.assertAlmostEqual(tools.wind._ms_to_kmhr(27.77777778), 100)
        self.assertAlmostEqual(tools.wind._ms_to_kmhr(10), 36)
        self.assertAlmostEqual(tools.wind._ms_to_kmhr(2), 7.2)
