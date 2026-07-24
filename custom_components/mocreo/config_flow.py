import voluptuous as vol
import aiohttp
import logging
from typing import Any

from homeassistant import config_entries
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD, CONF_API_KEY
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN, CONF_ASSET_ID

_LOGGER = logging.getLogger(__name__)

# Base API URL
BASE_URL = "https://api.mocreo.com/v1"

class MocreoConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for MOCREO IoT Platform."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize the config flow."""
        self._email: str | None = None
        self._token: str | None = None
        self._assets: list[dict[str, Any]] = []

    async def _async_make_request(
        self, session: aiohttp.ClientSession, url: str, method: str = "GET", headers: dict = None, json_data: dict = None
    ) -> dict[str, Any]:
        """Make an HTTP request and return parsed JSON."""
        try:
            async with session.request(method, url, headers=headers, json=json_data, timeout=10) as response:
                if 200 <= response.status < 300:
                    return await response.json()
                elif response.status in (400, 401):
                    raise InvalidAuth
                elif response.status == 403:
                    raise Forbidden
                elif response.status == 404:
                    raise NotFound
                else:
                    _LOGGER.error("Mocreo API returned unexpected status %s for url %s", response.status, url)
                    raise CannotConnect
        except aiohttp.ClientError as err:
            _LOGGER.error("Connection error to %s: %s", url, err)
            raise CannotConnect from err

    async def async_step_user(self, user_input=None):
        """Handle the login step where user enters email and password."""
        errors = {}

        if user_input is not None:
            email = user_input[CONF_EMAIL]
            password = user_input[CONF_PASSWORD]
            self._email = email

            session = async_get_clientsession(self.hass)

            try:
                # 1. Login to get access token
                login_url = f"{BASE_URL}/users/login"
                login_data = {"email": email, "password": password}
                login_res = await self._async_make_request(session, login_url, "POST", json_data=login_data)
                
                if not login_res.get("success"):
                    raise InvalidAuth
                
                # Retrieve the token (access_token or token)
                token = login_res.get("result", {}).get("access_token") or login_res.get("result", {}).get("token")
                if not token:
                    _LOGGER.error("Failed to find token in login response: %s", login_res)
                    raise UnknownError
                
                self._token = token
                headers = {"Authorization": f"Bearer {self._token}"}

                # 2. Get list of assets
                assets_url = f"{BASE_URL}/assets"
                assets_res = await self._async_make_request(session, assets_url, headers=headers)
                
                if not assets_res.get("success"):
                    raise UnknownError

                self._assets = assets_res.get("result", [])
                if not self._assets:
                    errors["base"] = "no_assets"
                elif len(self._assets) == 1:
                    # Single asset: auto-select it and generate the API key
                    asset_id = self._assets[0]["id"]
                    asset_name = self._assets[0].get("displayName", "My Asset")
                    return await self._async_create_key_and_entry(asset_id, asset_name)
                else:
                    # Multiple assets: transition to select asset step
                    return await self.async_step_select_asset()

            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except Forbidden:
                errors["base"] = "forbidden"
            except NotFound:
                errors["base"] = "invalid_asset"
            except Exception as err:
                _LOGGER.exception("Unexpected error in config flow login: %s", err)
                errors["base"] = "unknown"

        data_schema = vol.Schema({
            vol.Required(CONF_EMAIL): str,
            vol.Required(CONF_PASSWORD): str,
        })

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )

    async def async_step_select_asset(self, user_input=None):
        """Step to select an asset if multiple are present."""
        errors = {}

        if user_input is not None:
            asset_id = user_input["asset_id"]
            # Find chosen asset name
            asset_name = next(
                (asset.get("displayName", "My Asset") for asset in self._assets if asset["id"] == asset_id),
                "My Asset"
            )
            try:
                return await self._async_create_key_and_entry(asset_id, asset_name)
            except Exception as err:
                _LOGGER.exception("Error generating API key: %s", err)
                errors["base"] = "api_key_failed"

        # Map IDs to names for the dropdown UI selector
        asset_options = {
            asset["id"]: asset.get("displayName") or f"Asset {asset['id'][:8]}"
            for asset in self._assets
        }

        data_schema = vol.Schema({
            vol.Required("asset_id"): vol.In(asset_options),
        })

        return self.async_show_form(
            step_id="select_asset", data_schema=data_schema, errors=errors
        )

    async def _async_create_key_and_entry(self, asset_id: str, asset_name: str):
        """Create a permanent API Key and return the config entry creation step."""
        session = async_get_clientsession(self.hass)
        headers = {"Authorization": f"Bearer {self._token}"}
        url = f"{BASE_URL}/assets/{asset_id}/apikeys"
        
        payload = {
            "displayName": "Home Assistant Integration",
            "permissions": [
                "asset.read",
                "asset.update",
                "device.read",
                "device.update",
                "membership.read"
            ],
            "expiresAt": None
        }

        res = await self._async_make_request(session, url, "POST", headers=headers, json_data=payload)
        if not res.get("success"):
            raise UnknownError

        api_key = res.get("result", {}).get("key")
        if not api_key:
            raise UnknownError

        return self.async_create_entry(
            title=f"Mocreo: {asset_name}",
            data={
                CONF_API_KEY: api_key,
                CONF_ASSET_ID: asset_id,
            }
        )

class CannotConnect(Exception):
    """Error to indicate we cannot connect."""

class InvalidAuth(Exception):
    """Error to indicate there is invalid auth."""

class Forbidden(Exception):
    """Error to indicate permissions are insufficient."""

class NotFound(Exception):
    """Error to indicate the resource was not found."""

class UnknownError(Exception):
    """Generic error fallback."""
