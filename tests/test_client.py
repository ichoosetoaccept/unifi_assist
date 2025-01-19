import pytest
import aiohttp
from unittest.mock import AsyncMock, patch
import pytest_asyncio
from unifi_assist.client import UniFiClient
import os

# Test data
TEST_HOST = "unifi.example.com"
TEST_API_KEY = "test-api-key"
TEST_SITE = "default"

@pytest.fixture(autouse=True)
def clear_env(monkeypatch):
    """Clear environment variables before each test."""
    monkeypatch.delenv("UNIFI_HOST", raising=False)
    monkeypatch.delenv("UNIFI_API_KEY", raising=False)

@pytest.fixture
def mock_env(monkeypatch):
    """Setup environment variables for testing."""
    monkeypatch.setenv("UNIFI_HOST", TEST_HOST)
    monkeypatch.setenv("UNIFI_API_KEY", TEST_API_KEY)

@pytest_asyncio.fixture
async def client():
    """Create a test client instance."""
    client = UniFiClient(TEST_HOST, TEST_API_KEY)
    # Initialize the client session
    await client._ensure_client()
    try:
        yield client
    finally:
        await client.close()

@pytest.fixture
def mock_response():
    """Create a mock response."""
    response = AsyncMock()
    response.json = AsyncMock()  # Return value will be set in each test
    response.raise_for_status = AsyncMock()  # No error by default
    response.__aenter__ = AsyncMock()
    response.__aexit__ = AsyncMock()
    response.__aenter__.return_value = response
    return response

@pytest.mark.asyncio
async def test_client_init():
    """Test client initialization with explicit parameters."""
    client = UniFiClient(TEST_HOST, TEST_API_KEY)
    assert client.host == TEST_HOST
    assert client.api_key == TEST_API_KEY
    assert client.base_url == f"https://{TEST_HOST}"
    await client.close()

@pytest.mark.asyncio
async def test_client_init_from_env(mock_env):
    """Test client initialization from environment variables."""
    client = UniFiClient()
    assert client.host == TEST_HOST
    assert client.api_key == TEST_API_KEY
    await client.close()

@pytest.mark.asyncio
async def test_client_init_missing_host():
    """Test client initialization with missing host."""
    with pytest.raises(ValueError, match="Host must be provided or set in UNIFI_HOST environment variable"):
        UniFiClient(api_key=TEST_API_KEY)

@pytest.mark.asyncio
async def test_client_init_missing_api_key():
    """Test client initialization with missing API key."""
    with pytest.raises(ValueError, match="API key must be provided or set in UNIFI_API_KEY environment variable"):
        UniFiClient(host=TEST_HOST)

@pytest.mark.asyncio
async def test_get_sites(client, mock_response):
    """Test getting sites."""
    mock_response.json.return_value = [
        {"name": "default", "desc": "Default"},
        {"name": "site2", "desc": "Site 2"}
    ]
    
    with patch.object(client.client, "get", return_value=mock_response):
        sites = await client.get_sites()
        assert len(sites) == 2
        assert sites[0]["name"] == "default"
        client.client.get.assert_called_once_with("/proxy/network/integration/v1/sites", ssl=True)

@pytest.mark.asyncio
async def test_get_device_stats(client, mock_response):
    """Test getting device statistics."""
    mock_response.json.return_value = {"data": [
        {"name": "device1", "status": "online"},
        {"name": "device2", "status": "offline"}
    ]}
    
    with patch.object(client.client, "get", return_value=mock_response):
        stats = await client.get_device_stats(TEST_SITE)
        assert len(stats) == 2
        assert stats[0]["name"] == "device1"
        client.client.get.assert_called_once_with(f"/proxy/network/api/s/{TEST_SITE}/stat/device", ssl=True)

@pytest.mark.asyncio
async def test_get_client_stats(client, mock_response):
    """Test getting client statistics."""
    mock_response.json.return_value = {"data": [
        {"hostname": "client1", "is_wired": True},
        {"hostname": "client2", "is_wired": False}
    ]}
    
    with patch.object(client.client, "get", return_value=mock_response):
        stats = await client.get_client_stats(TEST_SITE)
        assert len(stats) == 2
        assert stats[0]["hostname"] == "client1"
        client.client.get.assert_called_once_with(f"/proxy/network/api/s/{TEST_SITE}/stat/sta", ssl=True)

@pytest.mark.asyncio
async def test_get_network_health(client, mock_response):
    """Test getting network health."""
    mock_response.json.return_value = {"data": {
        "status": "good",
        "subsystems": {"wan": "ok", "lan": "ok"}
    }}
    
    with patch.object(client.client, "get", return_value=mock_response):
        health = await client.get_network_health(TEST_SITE)
        assert health["status"] == "good"
        client.client.get.assert_called_once_with(f"/proxy/network/api/s/{TEST_SITE}/stat/health", ssl=True)

@pytest.mark.asyncio
async def test_get_system_info(client, mock_response):
    """Test getting system information."""
    mock_response.json.return_value = {"data": {
        "version": "7.0.0",
        "build": "12345"
    }}
    
    with patch.object(client.client, "get", return_value=mock_response):
        info = await client.get_system_info(TEST_SITE)
        assert info["version"] == "7.0.0"
        client.client.get.assert_called_once_with(f"/proxy/network/api/s/{TEST_SITE}/stat/sysinfo", ssl=True)

@pytest.mark.asyncio
async def test_http_error_handling(client):
    """Test HTTP error handling."""
    error_response = AsyncMock()
    error_response.raise_for_status = AsyncMock(side_effect=aiohttp.ClientError("HTTP Error"))
    error_response.__aenter__.return_value = error_response
    
    with patch.object(client.client, "get", return_value=error_response):
        with pytest.raises(aiohttp.ClientError):
            await client.get_sites()

@pytest.mark.asyncio
async def test_context_manager():
    """Test async context manager."""
    async with UniFiClient(TEST_HOST, TEST_API_KEY) as client:
        assert client.client is not None
    assert client.client is None
