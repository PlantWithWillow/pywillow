"""Tests for Willow exceptions."""

import pytest

from pywillow import WillowApiError, WillowAuthError, WillowError


def test_willow_error_is_base() -> None:
    """WillowError is the base exception."""
    assert issubclass(WillowAuthError, WillowError)
    assert issubclass(WillowApiError, WillowError)


def test_willow_auth_error() -> None:
    """WillowAuthError can be raised and caught."""
    with pytest.raises(WillowAuthError, match="failed"):
        raise WillowAuthError("Authentication failed")


def test_willow_api_error_with_status() -> None:
    """WillowApiError stores the HTTP status code."""
    err = WillowApiError("Server error", status=500)
    assert err.status == 500
    assert "Server error" in str(err)


def test_willow_api_error_without_status() -> None:
    """WillowApiError works without a status code."""
    err = WillowApiError("Something went wrong")
    assert err.status is None
