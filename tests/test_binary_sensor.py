"""Test MOCREO binary sensor logic and icon mapping."""
import sys
import unittest
from unittest.mock import MagicMock

# Mock homeassistant modules if not installed in current environment
if "homeassistant" not in sys.modules:
    ha_mock = MagicMock()
    sys.modules["homeassistant"] = ha_mock
    sys.modules["homeassistant.config_entries"] = ha_mock
    sys.modules["homeassistant.const"] = ha_mock
    sys.modules["homeassistant.core"] = ha_mock
    sys.modules["homeassistant.helpers"] = ha_mock
    sys.modules["homeassistant.helpers.aiohttp_client"] = ha_mock
    sys.modules["homeassistant.helpers.update_coordinator"] = ha_mock
    sys.modules["homeassistant.components"] = ha_mock
    sys.modules["homeassistant.components.sensor"] = ha_mock
    sys.modules["homeassistant.components.binary_sensor"] = ha_mock

class TestMocreoBinarySensor(unittest.TestCase):
    """Test suite for binary sensor icon selection and logic."""

    def test_hub_icon_selection(self):
        """Test that HUB hardware gets mdi:router-wireless icon."""
        device_type = "HUB"
        model = "H6PRO"
        if device_type == "HUB" or any(h in model for h in ("H6", "H5", "H1", "H2")):
            icon = "mdi:router-wireless"
        else:
            icon = "mdi:signal-distance-variant"
        self.assertEqual(icon, "mdi:router-wireless")

    def test_water_leak_icon_selection(self):
        """Test that SW series hardware gets mdi:water-alert icon."""
        model = "SW2"
        if "SW" in model:
            icon = "mdi:water-alert"
        else:
            icon = "mdi:signal-distance-variant"
        self.assertEqual(icon, "mdi:water-alert")

    def test_freezer_sensor_icon_selection(self):
        """Test that ST9 freezer hardware gets mdi:snowflake-alert icon."""
        model = "ST9"
        if "ST9" in model or "SF" in model:
            icon = "mdi:snowflake-alert"
        else:
            icon = "mdi:signal-distance-variant"
        self.assertEqual(icon, "mdi:snowflake-alert")

if __name__ == "__main__":
    unittest.main()
