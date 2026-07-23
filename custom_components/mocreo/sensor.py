"""Support for MOCREO IoT Platform sensors."""
import logging
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE, UnitOfTemperature
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
    """Set up MOCREO sensors based on a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    entities: list[SensorEntity] = []

    # Dynamically discover which properties are available for each device
    for device_id, device in coordinator.data.items():
        properties = device.get("properties", {})
        
        if "temperature" in properties:
            entities.append(MocreoSensor(coordinator, device_id, "temperature"))
        if "humidity" in properties:
            entities.append(MocreoSensor(coordinator, device_id, "humidity"))
        if "battery_percentage" in properties:
            entities.append(MocreoSensor(coordinator, device_id, "battery_percentage"))

    async_add_entities(entities)

class MocreoSensor(CoordinatorEntity, SensorEntity):
    """Representation of a MOCREO sensor."""

    def __init__(self, coordinator, device_id: str, sensor_type: str) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device_id = device_id
        self._sensor_type = sensor_type
        
        # Configure configuration depending on sensor type
        if sensor_type == "temperature":
            self._attr_name = "Temperature"
            self._attr_device_class = SensorDeviceClass.TEMPERATURE
            self._attr_state_class = SensorStateClass.MEASUREMENT
            self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
            self._attr_icon = "mdi:thermometer"
        elif sensor_type == "humidity":
            self._attr_name = "Humidity"
            self._attr_device_class = SensorDeviceClass.HUMIDITY
            self._attr_state_class = SensorStateClass.MEASUREMENT
            self._attr_native_unit_of_measurement = PERCENTAGE
            self._attr_icon = "mdi:water-percent"
        elif sensor_type == "battery_percentage":
            self._attr_name = "Battery"
            self._attr_device_class = SensorDeviceClass.BATTERY
            self._attr_state_class = SensorStateClass.MEASUREMENT
            self._attr_native_unit_of_measurement = PERCENTAGE
            self._attr_icon = "mdi:battery"
            
        self._attr_unique_id = f"mocreo_{device_id}_{sensor_type}"
        self._attr_has_entity_name = True

    @property
    def native_value(self) -> Any:
        """Return the state of the sensor."""
        device = self.coordinator.data.get(self._device_id)
        if device:
            val = device.get("properties", {}).get(self._sensor_type)
            if val is not None:
                if self._sensor_type in ("temperature", "humidity"):
                    return val / 100.0
                return val
        return None

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
