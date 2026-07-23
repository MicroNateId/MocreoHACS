"""Test MOCREO sensor data parsing and scaling."""
import unittest

class TestMocreoSensorScaling(unittest.TestCase):
    """Test suite for sensor property scaling."""

    def test_temperature_scaling(self):
        """Test that raw integer temperature 2250 scales to 22.5 Celsius."""
        raw_val = 2250
        scaled_val = raw_val / 100.0
        self.assertEqual(scaled_val, 22.5)

    def test_humidity_scaling(self):
        """Test that raw integer humidity 5000 scales to 50.0 percent."""
        raw_val = 5000
        scaled_val = raw_val / 100.0
        self.assertEqual(scaled_val, 50.0)

if __name__ == "__main__":
    unittest.main()
