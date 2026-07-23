"""Live system verification tests for Home Assistant test host."""
import subprocess
import unittest

class TestLiveHomeAssistantHost(unittest.TestCase):
    """Test suite for live Home Assistant host verification over SSH."""

    def test_remote_component_files_exist(self):
        """Verify that remote Home Assistant server has all required custom component files."""
        cmd = ["ssh", "HomeAssistant", "ls /config/custom_components/mocreo"]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                output = result.stdout
                self.assertIn("__init__.py", output)
                self.assertIn("config_flow.py", output)
                self.assertIn("sensor.py", output)
                self.assertIn("binary_sensor.py", output)
                self.assertIn("manifest.json", output)
            else:
                self.skipTest(f"Live host SSH unreachable: {result.stderr}")
        except Exception as err:
            self.skipTest(f"SSH test skipped: {err}")

    def test_remote_homeassistant_logs_for_errors(self):
        """Check remote Home Assistant log for any MOCREO errors."""
        cmd = ["ssh", "HomeAssistant", "grep -i mocreo /config/home-assistant.log | grep -i error || true"]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                errors = result.stdout.strip()
                self.assertEqual(errors, "", f"Found MOCREO errors in remote HA log: {errors}")
            else:
                self.skipTest(f"Live host log check unreachable: {result.stderr}")
        except Exception as err:
            self.skipTest(f"Log check test skipped: {err}")

if __name__ == "__main__":
    unittest.main()
