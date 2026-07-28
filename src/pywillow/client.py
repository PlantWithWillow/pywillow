"""Async client for the Willow API."""

from typing import Any, cast

from aiohttp import ClientResponseError, ClientSession, ClientTimeout

from pywillow.const import DEFAULT_TIMEOUT, DEVICES_URL, PROFILE_URL
from pywillow.exceptions import WillowApiError, WillowAuthError
from pywillow.models import WillowDevice, WillowProfile


class WillowClient:
    """Async client for the Willow API."""

    def __init__(
        self,
        session: ClientSession,
        token: str,
        *,
        base_url: str | None = None,
    ) -> None:
        """Initialize the Willow client.

        Args:
            session: An aiohttp ClientSession.
            token: OAuth2 bearer access token.
            base_url: Override the default API base URL (for testing).
        """
        self._session = session
        self._token = token
        if base_url:
            self._profile_url = f"{base_url}/api/v1/profiles/short/"
            self._devices_url = f"{base_url}/api/v1b/sensor/paired/"
        else:
            self._profile_url = PROFILE_URL
            self._devices_url = DEVICES_URL

    def update_token(self, token: str) -> None:
        """Update the access token (e.g. after a refresh)."""
        self._token = token

    async def get_profile(self) -> WillowProfile:
        """Get the authenticated user's profile."""
        return cast(WillowProfile, await self._async_request("GET", self._profile_url))

    async def get_devices(self) -> list[WillowDevice]:
        """Get the user's paired sensor devices."""
        return cast(
            list[WillowDevice],
            await self._async_request("GET", self._devices_url),
        )

    async def _async_request(self, method: str, url: str) -> Any:
        """Make an authenticated request to the Willow API."""
        headers = {"Authorization": f"Bearer {self._token}"}
        try:
            async with self._session.request(
                method,
                url,
                headers=headers,
                raise_for_status=True,
                timeout=ClientTimeout(total=DEFAULT_TIMEOUT),
            ) as resp:
                return await resp.json()
        except ClientResponseError as err:
            if err.status in (401, 403):
                raise WillowAuthError(f"Authentication failed: {err.status}") from err
            raise WillowApiError(f"API request failed: {err.status}", status=err.status) from err
