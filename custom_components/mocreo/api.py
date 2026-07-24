"""API Client for MOCREO OpenAPI."""
import logging
from typing import Any
import aiohttp

_LOGGER = logging.getLogger(__name__)
BASE_URL = "https://api.mocreo.com/v1"

class MocreoApiClient:
    """ApiClient for MOCREO OpenAPI."""

    def __init__(self, api_key: str, session: aiohttp.ClientSession | None = None) -> None:
        """Initialize the API client."""
        self._api_key = api_key
        self._session = session

    async def async_get_devices(self) -> dict[str, dict[str, Any]]:
        """Fetch all devices for the account and parse properties/attributes."""
        close_session = False
        if self._session is None:
            session = aiohttp.ClientSession()
            close_session = True
        else:
            session = self._session

        url = f"{BASE_URL}/devices"
        headers = {"Authorization": f"Bearer {self._api_key}"}

        try:
            async with session.get(url, headers=headers, timeout=10) as response:
                if response.status != 200:
                    _LOGGER.error("Mocreo API returned status %s for url %s", response.status, url)
                    return {}

                data = await response.json()
                if not data.get("success"):
                    _LOGGER.error("Mocreo API returned error: %s", data)
                    return {}

                devices_list = data.get("result", [])
                devices_dict = {}

                for dev in devices_list:
                    dev_id = dev.get("id")
                    if not dev_id:
                        continue

                    props = {}
                    for p in dev.get("properties", []):
                        name = p.get("name")
                        val = p.get("value")
                        if name:
                            props[name] = val

                    attrs = dev.get("attributes", {})

                    devices_dict[dev_id] = {
                        "id": dev_id,
                        "name": attrs.get("displayName") or dev.get("name") or f"Mocreo {dev.get('model')}",
                        "model": dev.get("model"),
                        "type": dev.get("type"),
                        "properties": props,
                        "attributes": attrs,
                    }

                return devices_dict
        except Exception as err:
            _LOGGER.exception("Error communicating with MOCREO API: %s", err)
            return {}
        finally:
            if close_session:
                await session.close()
