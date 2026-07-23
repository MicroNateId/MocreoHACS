"""The MOCREO IoT Platform integration."""
from datetime import timedelta
import logging
import asyncio

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_API_KEY, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, CONF_ASSET_ID, DEFAULT_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.BINARY_SENSOR]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up MOCREO IoT Platform from a config entry."""
    api_key = entry.data.get(CONF_API_KEY)
    asset_id = entry.data.get(CONF_ASSET_ID)

    _LOGGER.debug("Setting up MOCREO entry: asset_id=%s", asset_id)
    if not asset_id:
        _LOGGER.error("MOCREO Asset ID is missing or empty in configuration!")
        return False

    session = async_get_clientsession(hass)

    async def async_update_data():
        """Fetch data from Mocreo API."""
        url = f"https://api.mocreo.com/v1/assets/{asset_id}/devices"
        headers = {"X-API-Key": api_key}
        
        try:
            async with asyncio.timeout(10):
                async with session.get(url, headers=headers) as response:
                    if response.status != 200:
                        raise UpdateFailed(f"Error communicating with API: status {response.status}")
                    data = await response.json()
                    if not data.get("success"):
                        raise UpdateFailed(f"API returned failure: {data.get('errors')}")
                    
                    # Store device dictionary keyed by device ID
                    devices = {}
                    for dev in data.get("result", []):
                        devices[dev["id"]] = dev
                    return devices
        except Exception as err:
            raise UpdateFailed(f"Error fetching data: {err}") from err

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=DOMAIN,
        update_method=async_update_data,
        update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
    )

    # Fetch initial data
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    # Register static path for custom Lovelace card
    try:
        hass.http.register_static_path(
            "/mocreo_static/mocreo-card.js",
            hass.config.path("custom_components/mocreo/mocreo-card.js"),
            cache_headers=False,
        )
    except Exception:
        pass

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
