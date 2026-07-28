"""Exceptions for the Willow API client."""


class WillowError(Exception):
    """Base exception for Willow API errors."""


class WillowAuthError(WillowError):
    """Exception raised when authentication fails."""


class WillowApiError(WillowError):
    """Exception raised when an API request fails."""

    def __init__(self, message: str, status: int | None = None) -> None:
        """Initialize the error."""
        super().__init__(message)
        self.status = status
