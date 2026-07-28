"""Constants for the Willow API client."""

BASE_URL = "https://api.plantwithwillow.com.au"

OAUTH2_AUTHORIZE_URL = f"{BASE_URL}/oauth/authorize/"
OAUTH2_TOKEN_URL = f"{BASE_URL}/oauth/token/"

PROFILE_URL = f"{BASE_URL}/api/v1/profiles/short/"
DEVICES_URL = f"{BASE_URL}/api/v1b/sensor/paired/"

DEFAULT_TIMEOUT = 30
