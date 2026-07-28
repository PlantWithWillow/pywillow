"""Tests for Willow data models."""

from pywillow.models import WillowDevice, WillowProfile, WillowReading, WillowUserPlant


def test_willow_profile() -> None:
    """WillowProfile TypedDict accepts valid data."""
    profile: WillowProfile = {
        "id": 1,
        "username": "user@example.com",
        "profile_image": None,
    }
    assert profile["id"] == 1
    assert profile["username"] == "user@example.com"


def test_willow_user_plant() -> None:
    """WillowUserPlant TypedDict accepts valid data."""
    plant: WillowUserPlant = {
        "id": 10,
        "name": "Basil",
        "location": "Kitchen",
    }
    assert plant["name"] == "Basil"
    assert plant["location"] == "Kitchen"


def test_willow_reading() -> None:
    """WillowReading TypedDict accepts valid data."""
    reading: WillowReading = {
        "timestamp": "2026-05-08T12:00:00+00:00",
        "temperature": 21.5,
        "humidity": 55.0,
        "moisture": 30.0,
        "light": 1200.0,
    }
    assert reading["temperature"] == 21.5
    assert reading["light"] == 1200.0


def test_willow_device_with_reading() -> None:
    """WillowDevice TypedDict accepts a device with a latest reading."""
    device: WillowDevice = {
        "id": 1,
        "sensor_id": "SENSOR123",
        "battery_life": 88,
        "version": "1.2.3",
        "user_plant": {
            "id": 10,
            "name": "Basil",
            "location": "Kitchen",
        },
        "latest_reading": {
            "timestamp": "2026-05-08T12:00:00+00:00",
            "temperature": 21.5,
            "humidity": 55.0,
            "moisture": 30.0,
            "light": 1200.0,
        },
    }
    assert device["sensor_id"] == "SENSOR123"
    assert device["latest_reading"] is not None
    assert device["latest_reading"]["temperature"] == 21.5


def test_willow_device_without_reading() -> None:
    """WillowDevice TypedDict accepts a device with no reading."""
    device: WillowDevice = {
        "id": 2,
        "sensor_id": "SENSOR456",
        "battery_life": None,
        "version": None,
        "user_plant": {
            "id": 11,
            "name": "Mint",
            "location": None,
        },
        "latest_reading": None,
    }
    assert device["battery_life"] is None
    assert device["latest_reading"] is None


def test_willow_device_optional_profile_image() -> None:
    """WillowDevice TypedDict allows omitting profile_image."""
    device: WillowDevice = {
        "id": 3,
        "sensor_id": "SENSOR789",
        "battery_life": 50,
        "version": "2.0",
        "user_plant": {
            "id": 12,
            "name": "Rosemary",
            "location": "Balcony",
        },
        "latest_reading": None,
    }
    assert "profile_image" not in device
