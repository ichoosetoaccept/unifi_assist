import os
import pytest
import pytest_asyncio
from unifi_assist.client import UniFiClient

# These are required for the tests to run
TEST_HOST = os.getenv("UNIFI_HOST")
TEST_API_KEY = os.getenv("UNIFI_API_KEY")

# Skip all tests if credentials are not set
pytestmark = pytest.mark.skipif(
    not (TEST_HOST and TEST_API_KEY),
    reason="UNIFI_HOST and UNIFI_API_KEY environment variables must be set to run tests",
)


@pytest_asyncio.fixture
async def client():
    """Fixture that provides a UniFiClient instance."""
    async with UniFiClient(
        host=TEST_HOST, api_key=TEST_API_KEY, verify_ssl=False
    ) as client:
        yield client


@pytest.mark.asyncio
async def test_client_initialization(monkeypatch):
    """Test client initialization with different parameters."""
    # Remove environment variables to test explicit parameters
    monkeypatch.delenv("UNIFI_HOST", raising=False)
    monkeypatch.delenv("UNIFI_API_KEY", raising=False)

    # Test with explicit parameters
    async with UniFiClient(host=TEST_HOST, api_key=TEST_API_KEY) as client:
        assert client.host == TEST_HOST
        assert client.api_key == TEST_API_KEY
        assert client.verify_ssl is True  # default value

    # Test with invalid parameters
    with pytest.raises(ValueError, match="Host must be provided"):
        UniFiClient(host=None, api_key=TEST_API_KEY)

    with pytest.raises(ValueError, match="API key must be provided"):
        UniFiClient(host=TEST_HOST, api_key=None)


@pytest.mark.asyncio
async def test_get_system_info(client):
    """Test getting system information."""
    response = await client.get_system_info()
    assert isinstance(response, dict)
    # Basic structure validation
    assert "applicationVersion" in response


@pytest.mark.asyncio
async def test_get_sites(client):
    """Test getting list of sites."""
    response = await client.get_sites()
    assert isinstance(response, dict)
    # The response should contain a list of sites
    assert "sites" in response or isinstance(response.get("data", []), list)


@pytest.mark.asyncio
async def test_get_devices(client):
    """Test getting devices for a site."""
    # First get sites to get a valid site_id
    sites_response = await client.get_sites()
    sites = sites_response.get("sites", []) or sites_response.get("data", [])
    assert sites, "No sites found to test with"

    site_id = sites[0].get("id")
    assert site_id, "Could not get site_id from response"

    devices_response = await client.get_devices(site_id)
    assert isinstance(devices_response, dict)
    # The response should contain a list of devices
    assert "devices" in devices_response or isinstance(
        devices_response.get("data", []), list
    )


@pytest.mark.asyncio
async def test_get_clients(client):
    """Test getting clients for a site."""
    sites_response = await client.get_sites()
    sites = sites_response.get("sites", []) or sites_response.get("data", [])
    assert sites, "No sites found to test with"

    site_id = sites[0].get("id")
    assert site_id, "Could not get site_id from response"

    clients_response = await client.get_clients(site_id)
    assert isinstance(clients_response, dict)
    # The response should contain a list of clients
    assert "clients" in clients_response or isinstance(
        clients_response.get("data", []), list
    )


@pytest.mark.asyncio
async def test_get_device_details_and_statistics(client):
    """Test getting device details and statistics."""
    sites_response = await client.get_sites()
    sites = sites_response.get("sites", []) or sites_response.get("data", [])
    assert sites, "No sites found to test with"

    site_id = sites[0].get("id")
    assert site_id, "Could not get site_id from response"

    # Get devices to get a valid device_id
    devices_response = await client.get_devices(site_id)
    devices = devices_response.get("devices", []) or devices_response.get("data", [])

    if not devices:
        pytest.skip("No devices found to test with")

    device_id = devices[0].get("id") or devices[0].get("deviceId")
    assert device_id, "Could not get device_id from response"

    # Test device details
    details_response = await client.get_device_details(site_id, device_id)
    assert isinstance(details_response, dict)

    # Test device statistics
    stats_response = await client.get_device_statistics(site_id, device_id)
    assert isinstance(stats_response, dict)


@pytest.mark.asyncio
async def test_invalid_site_id(client):
    """Test behavior with invalid site ID."""
    with pytest.raises(Exception):  # Should get an API error
        await client.get_devices("invalid_site_id")


@pytest.mark.asyncio
async def test_invalid_device_id(client):
    """Test behavior with invalid device ID."""
    # First get a valid site_id
    sites_response = await client.get_sites()
    sites = sites_response.get("sites", []) or sites_response.get("data", [])
    assert sites, "No sites found to test with"

    site_id = sites[0].get("id")
    assert site_id, "Could not get site_id from response"

    with pytest.raises(Exception):  # Should get an API error
        await client.get_device_details(site_id, "invalid_device_id")
