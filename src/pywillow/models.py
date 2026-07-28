"""Data models for the Willow API."""

from typing import NotRequired, TypedDict


class WillowProfile(TypedDict):
    """Willow profile response."""

    id: int
    username: str
    profile_image: str | None


class WillowUserPlant(TypedDict):
    """Willow user plant data."""

    id: int
    name: str
    location: str | None


class WillowReading(TypedDict):
    """Willow latest reading data."""

    timestamp: str
    temperature: float
    humidity: float
    moisture: float
    light: float


class WillowDevice(TypedDict):
    """Willow paired sensor data."""

    id: int
    sensor_id: str
    battery_life: int | float | None
    version: str | None
    user_plant: WillowUserPlant
    latest_reading: WillowReading | None
    profile_image: NotRequired[str | None]
