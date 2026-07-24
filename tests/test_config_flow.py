"""Test the MOCREO IoT Platform config flow."""
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

sys.modules["custom_components.mocreo.api"] = MagicMock()

class TestMocreoConfigFlow(unittest.TestCase):
    """Test suite for Mocreo Config Flow."""

    def test_sample_credential_validation(self):
        """Verify basic validation constants."""
        from custom_components.mocreo.const import DOMAIN, CONF_ASSET_ID, CONF_API_KEY
        self.assertEqual(DOMAIN, "mocreo")
        self.assertEqual(CONF_ASSET_ID, "asset_id")
        self.assertEqual(CONF_API_KEY, "api_key")

if __name__ == "__main__":
    unittest.main()
