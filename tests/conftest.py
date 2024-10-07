"""Global fixtures for Anova Nano integration."""
from unittest.mock import patch

import pytest
from pytest_socket import enable_socket, socket_allow_hosts

pytest_plugins = "pytest_homeassistant_custom_component"


@pytest.hookimpl(trylast=True)
def pytest_runtest_setup():
    """Ensure the bluetooth integration we depend on can load.

    https://github.com/MatthewFlamm/pytest-homeassistant-custom-component/issues/154#issuecomment-2065081783

    """
    enable_socket()
    socket_allow_hosts(
        # Allow "None" to allow the bluetooth integration to load.
        ["None"],
        allow_unix_socket=True,
    )


# This fixture is used to enable custom integrations, otherwise the custom_components folder will not be loaded.
@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):
    """Enable custom integrations."""
    yield


# This fixture is used to prevent HomeAssistant from attempting to create and dismiss persistent
# notifications. These calls would fail without this fixture since the persistent_notification
# integration is never loaded during a test.
@pytest.fixture(name="skip_notifications", autouse=True)
def skip_notifications_fixture():
    """Skip notification calls."""
    with patch("homeassistant.components.persistent_notification.async_create"), patch(
        "homeassistant.components.persistent_notification.async_dismiss"
    ):
        yield


# This fixture, when used, will result in calls to async_get_data to return None. To have the call
# return a value, we would add the `return_value=<VALUE_TO_RETURN>` parameter to the patch call.
# @pytest.fixture(name="bypass_get_data")
# def bypass_get_data_fixture():
#     """Skip calls to get data from API."""
#
#     async def mock_async_get_data(self):
#         return {"body": "test"}
#
#     with patch(
#         "custom_components.anova_nano.AnovaNanoApiClient.async_get_data",
#         mock_async_get_data,
#     ):
#         yield


# In this fixture, we are forcing calls to async_get_data to raise an Exception. This is useful
# for exception handling.
@pytest.fixture(name="error_on_get_data")
def error_get_data_fixture():
    """Simulate error when retrieving data from API."""
    # with patch(
    #     "custom_components.anova_nano.AnovaNanoApiClient.async_get_data",
    #     side_effect=AnovaNanoApiClientError,
    # ):
    yield
