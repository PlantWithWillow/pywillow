# pywillow

Async Python client for the [Willow](https://plantwithwillow.com.au/) plant sensor API.

## Installation

```bash
pip install pywillow
```

## Usage

```python
import aiohttp
from pywillow import WillowClient

async def main():
    async with aiohttp.ClientSession() as session:
        client = WillowClient(session, access_token="your-oauth2-token")

        # Get the authenticated user's profile
        profile = await client.get_profile()
        print(profile["username"])

        # Get paired sensor devices
        devices = await client.get_devices()
        for device in devices:
            print(device["sensor_id"], device["user_plant"]["name"])
```

## API

### `WillowClient(session, token, *, base_url=None)`

- **`update_token(token)`** — Update the access token (e.g. after an OAuth2 refresh).
- **`get_profile()`** → `WillowProfile` — Fetch the authenticated user's profile.
- **`get_devices()`** → `list[WillowDevice]` — Fetch the user's paired sensor devices.

### Models

All models are `TypedDict` subclasses representing the JSON responses from the Willow API:

- **`WillowProfile`** — `id`, `username`, `profile_image`
- **`WillowDevice`** — `id`, `sensor_id`, `battery_life`, `version`, `user_plant`, `latest_reading`, `profile_image` (optional)
- **`WillowUserPlant`** — `id`, `name`, `location`
- **`WillowReading`** — `timestamp`, `temperature`, `humidity`, `moisture`, `light`

### Exceptions

- **`WillowError`** — Base exception for all Willow API errors.
- **`WillowAuthError`** — Raised on 401/403 responses (authentication failed).
- **`WillowApiError`** — Raised on other HTTP errors. Includes a `status` attribute.

## Development

```bash
# Install with dev dependencies
uv sync

# Run tests
uv run pytest

# Build the package
uv build
```

## License

MIT
