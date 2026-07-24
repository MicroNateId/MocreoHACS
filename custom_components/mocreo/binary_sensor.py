"""Support for MOCREO IoT Platform binary sensors."""
import logging

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up MOCREO binary sensors based on a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    entities: list[BinarySensorEntity] = []

    # Expose online status binary sensors for all devices
    for device_id, device in coordinator.data.items():
        entities.append(MocreoOnlineBinarySensor(coordinator, device_id))

    async_add_entities(entities)

class MocreoOnlineBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Representation of a MOCREO online binary sensor."""

    def __init__(self, coordinator, device_id: str) -> None:
        """Initialize the binary sensor."""
        super().__init__(coordinator)
        self._device_id = device_id
        
        self._attr_name = "Online"
        self._attr_device_class = BinarySensorDeviceClass.CONNECTIVITY
        self._attr_unique_id = f"mocreo_{device_id}_online"
        self._attr_has_entity_name = True

    @property
    def is_on(self) -> bool:
        """Return true if the device is online."""
        device = self.coordinator.data.get(self._device_id)
        if device:
            return device.get("attributes", {}).get("online", False)
        return False

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        device = self.coordinator.data.get(self._device_id)
        if not device:
            return None
            
        labels = device.get("attributes", {}).get("labels", {})
        display_name = labels.get("displayName") or device.get("name") or f"Mocreo {device.get('model')} {self._device_id}"
        
        return DeviceInfo(
            identifiers={(DOMAIN, self._device_id)},
            name=display_name,
            manufacturer="MOCREO",
            model=device.get("model"),
        )
