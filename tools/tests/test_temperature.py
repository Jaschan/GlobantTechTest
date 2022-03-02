import unittest
from unittest.mock import patch, MagicMock, Mock
import tools

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
                self.assertAlmostEqual(tools.temperature.fahrenheit_to_celsius(f), c, delta=0.0001)

    def test_kelvin_to_celsius(self):
        for k, c, f in self.data:
            with self.subTest(k=k, c=c, f=f):
                self.assertAlmostEqual(tools.temperature.kelvin_to_celsius(k), c, delta=0.0001)

    def test_kelvin_to_fahrenheit(self):
        for k, c, f in self.data:
            with self.subTest(k=k, c=c, f=f):
                self.assertAlmostEqual(tools.temperature.kelvin_to_fahrenheit(k), f, delta=0.0001)
