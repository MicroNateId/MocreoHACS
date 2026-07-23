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

    for device_id, device in coordinator.data.items():
        # Connectivity / Online status for all devices
        entities.append(MocreoOnlineBinarySensor(coordinator, device_id))
        
        # Moisture / Water leak binary sensor if device reports water_leak property
        properties = device.get("properties", {})
        if "water_leak" in properties:
            entities.append(MocreoWaterLeakBinarySensor(coordinator, device_id))

    async_add_entities(entities)

class MocreoOnlineBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Representation of a MOCREO online binary sensor."""

    def __init__(self, coordinator, device_id: str) -> None:
        """Initialize the binary sensor."""
        super().__init__(coordinator)
        self._device_id = device_id
        
        device = self.coordinator.data.get(self._device_id, {})
        device_type = str(device.get("type", "")).upper()
        model = str(device.get("model", "")).upper()
        
        self._attr_name = "Online"
        self._attr_device_class = BinarySensorDeviceClass.CONNECTIVITY
        self._attr_unique_id = f"mocreo_{device_id}_online"
        self._attr_has_entity_name = True
        
        # Hardware model-specific icon selection across MOCREO product lines
        if device_type == "HUB" or any(h in model for h in ("H6", "H5", "H1", "H2")):
            self._attr_icon = "mdi:router-wireless"
        elif "SW" in model:
            self._attr_icon = "mdi:water-alert"
        elif "ST9" in model or "SF" in model:
            self._attr_icon = "mdi:snowflake-alert"
        elif "SL" in model:
            self._attr_icon = "mdi:sprout"
        elif "SC" in model:
            self._attr_icon = "mdi:door"
        elif any(s in model for s in ("ST", "LS")):
            self._attr_icon = "mdi:thermometer-water"
        else:
            self._attr_icon = "mdi:signal-distance-variant"

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

class MocreoWaterLeakBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Representation of a MOCREO water leak binary sensor."""

    def __init__(self, coordinator, device_id: str) -> None:
        """Initialize the water leak binary sensor."""
        super().__init__(coordinator)
        self._device_id = device_id
        
        self._attr_name = "Water Leak"
        self._attr_device_class = BinarySensorDeviceClass.MOISTURE
        self._attr_unique_id = f"mocreo_{device_id}_water_leak"
        self._attr_has_entity_name = True
        self._attr_icon = "mdi:water-alert"

    @property
    def is_on(self) -> bool:
        """Return true if water leak is detected."""
        device = self.coordinator.data.get(self._device_id)
        if device:
            val = device.get("properties", {}).get("water_leak")
            return bool(val)
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
