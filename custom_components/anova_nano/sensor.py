"""Sensor platform for Anova Nano."""
from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import AnovaNanoDataUpdateCoordinator
from .entity import AnovaNanoDescriptionEntity


@dataclass(frozen=True)
class AnovaSensorEntityDescription(SensorEntityDescription):
    """Describes Anova sensor entity."""


SENSOR_DESCRIPTIONS: tuple[AnovaSensorEntityDescription, ...] = (
    AnovaSensorEntityDescription(
        key="water_temp",
        name="water temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
        icon="mdi:thermometer-water",
    ),
    AnovaSensorEntityDescription(
        key="heater_temp",
        name="heater temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:thermometer",
    ),
    AnovaSensorEntityDescription(
        key="triac_temp",
        name="triac temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:thermometer",
    ),
    AnovaSensorEntityDescription(
        key="internal_temp",
        name="internal temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:thermometer",
    ),
    AnovaSensorEntityDescription(
        key="motor_speed",
        name="motor speed",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:fan",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_devices: AddEntitiesCallback
):
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices(
        AnovaNanoSensor(
            coordinator=coordinator,
            entity_description=entity_description,
        )
        for entity_description in SENSOR_DESCRIPTIONS
    )


class AnovaNanoSensor(AnovaNanoDescriptionEntity, SensorEntity):
    """anova_nano Sensor class."""

    def __init__(
        self,
        coordinator: AnovaNanoDataUpdateCoordinator,
        entity_description: AnovaSensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator, entity_description)
        self.entity_description = entity_description
        self.coordinator: AnovaNanoDataUpdateCoordinator = coordinator

    @property
    def native_value(self) -> str | None:
        """Return the native value of the sensor."""
        try:
            return getattr(self.coordinator.status, self.entity_description.key)
        except AttributeError:
            # Status is not set yet.
            return None
