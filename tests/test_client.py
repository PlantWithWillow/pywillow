"""Tests for the Willow API client."""

from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest

from pywillow import WillowApiError, WillowAuthError, WillowClient
from pywillow.models import WillowDevice, WillowProfile

PROFILE_DATA: WillowProfile = {
    "id": 42,
    "username": "garden@example.com",
    "profile_image": None,
}

DEVICES_DATA: list[WillowDevice] = [
    {
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
]


def _mock_response(data: Any, status: int = 200) -> MagicMock:
    """Build a mock aiohttp response context manager."""
    resp = MagicMock()
    resp.__aenter__ = AsyncMock(return_value=resp)
    resp.__aexit__ = AsyncMock(return_value=None)
    resp.json = AsyncMock(return_value=data)
    resp.status = status
    return resp


def _mock_error_response(status: int) -> MagicMock:
    """Build a mock aiohttp response that raises ClientResponseError."""
    from aiohttp import ClientResponseError

    resp = MagicMock()
    resp.__aenter__ = AsyncMock(
        side_effect=ClientResponseError(
            request_info=MagicMock(),
            history=(),
            status=status,
            message="error",
        )
    )
    resp.__aexit__ = AsyncMock(return_value=None)
    return resp


@pytest.mark.asyncio
async def test_get_profile() -> None:
    """get_profile returns the user profile."""
    session = MagicMock()
    session.request = MagicMock(return_value=_mock_response(PROFILE_DATA))

    client = WillowClient(session, "token")
    result = await client.get_profile()

    assert result == PROFILE_DATA
    assert result["id"] == 42
    assert result["username"] == "garden@example.com"


@pytest.mark.asyncio
async def test_get_devices() -> None:
    """get_devices returns the list of paired devices."""
    session = MagicMock()
    session.request = MagicMock(return_value=_mock_response(DEVICES_DATA))

    client = WillowClient(session, "token")
    result = await client.get_devices()

    assert len(result) == 1
    assert result[0]["sensor_id"] == "SENSOR123"
    assert result[0]["user_plant"]["name"] == "Basil"
    assert result[0]["latest_reading"]["temperature"] == 21.5


@pytest.mark.asyncio
async def test_update_token() -> None:
    """update_token changes the bearer token used in requests."""
    session = MagicMock()
    session.request = MagicMock(return_value=_mock_response(PROFILE_DATA))

    client = WillowClient(session, "old-token")
    client.update_token("new-token")
    await client.get_profile()

    call_args = session.request.call_args
    headers = call_args.kwargs["headers"]
    assert headers["Authorization"] == "Bearer new-token"


@pytest.mark.asyncio
async def test_auth_error_401() -> None:
    """A 401 response raises WillowAuthError."""
    session = MagicMock()
    session.request = MagicMock(return_value=_mock_error_response(401))

    client = WillowClient(session, "bad-token")
    with pytest.raises(WillowAuthError):
        await client.get_profile()


@pytest.mark.asyncio
async def test_auth_error_403() -> None:
    """A 403 response raises WillowAuthError."""
    session = MagicMock()
    session.request = MagicMock(return_value=_mock_error_response(403))

    client = WillowClient(session, "bad-token")
    with pytest.raises(WillowAuthError):
        await client.get_devices()


@pytest.mark.asyncio
async def test_api_error_500() -> None:
    """A 500 response raises WillowApiError."""
    session = MagicMock()
    session.request = MagicMock(return_value=_mock_error_response(500))

    client = WillowClient(session, "token")
    with pytest.raises(WillowApiError) as exc_info:
        await client.get_profile()

    assert exc_info.value.status == 500


@pytest.mark.asyncio
async def test_base_url_override() -> None:
    """Custom base_url is used for requests."""
    session = MagicMock()
    session.request = MagicMock(return_value=_mock_response(PROFILE_DATA))

    client = WillowClient(session, "token", base_url="https://custom.example.com")
    await client.get_profile()

    call_args = session.request.call_args
    assert "custom.example.com" in call_args.args[1]


@pytest.mark.asyncio
async def test_get_devices_empty() -> None:
    """get_devices returns an empty list when no devices are paired."""
    session = MagicMock()
    session.request = MagicMock(return_value=_mock_response([]))

    client = WillowClient(session, "token")
    result = await client.get_devices()

    assert result == []
