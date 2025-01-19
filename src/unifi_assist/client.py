from typing import Optional
import aiohttp
import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class UniFiClient:
    """Client for interacting with the UniFi Network API."""

    def __init__(
        self,
        host: Optional[str] = None,
        api_key: Optional[str] = None,
        verify_ssl: bool = True,
        logger: Optional[logging.Logger] = None,
    ):
        """Initialize the UniFi client.

        Args:
            host: UniFi Network Application host (e.g. 192.168.1.1)
            api_key: API key for authentication
            verify_ssl: Whether to verify SSL certificates
            logger: Logger instance
        """
        self.host = host or os.getenv("UNIFI_HOST")
        if not self.host:
            raise ValueError(
                "Host must be provided or set in UNIFI_HOST environment variable"
            )

        self.api_key = api_key or os.getenv("UNIFI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key must be provided or set in UNIFI_API_KEY environment variable"
            )

        self.verify_ssl = verify_ssl
        self.logger = logger or logging.getLogger("unifi_client")
        self.logger.debug(f"Initializing UniFi client for host: {self.host}")

        self.session = aiohttp.ClientSession(
            headers={"Accept": "application/json", "X-API-KEY": self.api_key}
        )

    async def close(self):
        """Close the client session."""
        await self.session.close()

    async def _get(self, endpoint: str) -> dict:
        """Make a GET request to the UniFi API.

        Args:
            endpoint: API endpoint path

        Returns:
            Response data as a dictionary
        """
        url = f"https://{self.host}/{endpoint}"
        async with self.session.get(url, ssl=self.verify_ssl) as response:
            response.raise_for_status()
            return await response.json()

    async def _post(self, endpoint: str, data: dict) -> dict:
        """Make a POST request to the UniFi API.

        Args:
            endpoint: API endpoint path
            data: Request body data

        Returns:
            Response data as a dictionary
        """
        url = f"https://{self.host}/{endpoint}"
        async with self.session.post(url, json=data, ssl=self.verify_ssl) as response:
            response.raise_for_status()
            return await response.json()

    async def get_sites(self) -> dict:
        """Get list of all sites.

        Returns:
            List of sites
        """
        return await self._get("proxy/network/integration/v1/sites")

    async def get_devices(self, site_id: str) -> dict:
        """Get list of all devices in a site.

        Args:
            site_id: Site identifier

        Returns:
            List of devices
        """
        return await self._get(f"proxy/network/integration/v1/sites/{site_id}/devices")

    async def get_device_details(self, site_id: str, device_id: str) -> dict:
        """Get detailed information about a specific device.

        Args:
            site_id: Site identifier
            device_id: Device identifier

        Returns:
            Device details
        """
        return await self._get(
            f"proxy/network/integration/v1/sites/{site_id}/devices/{device_id}"
        )

    async def get_device_statistics(self, site_id: str, device_id: str) -> dict:
        """Get statistics for a specific device.

        Args:
            site_id: Site identifier
            device_id: Device identifier

        Returns:
            Device statistics
        """
        return await self._get(
            f"proxy/network/integration/v1/sites/{site_id}/devices/{device_id}/statistics/latest"
        )

    async def perform_device_action(
        self, site_id: str, device_id: str, action: dict
    ) -> dict:
        """Perform an action on a specific device.

        Args:
            site_id: Site identifier
            device_id: Device identifier
            action: Action data

        Returns:
            Response from the action
        """
        return await self._post(
            f"proxy/network/integration/v1/sites/{site_id}/devices/{device_id}/actions",
            action,
        )

    async def get_clients(self, site_id: str) -> dict:
        """Get list of all clients in a site.

        Args:
            site_id: Site identifier

        Returns:
            List of clients
        """
        return await self._get(f"proxy/network/integration/v1/sites/{site_id}/clients")

    async def get_system_info(self) -> dict:
        """Get system information.

        Returns:
            System information
        """
        return await self._get("proxy/network/integration/v1/info")

    async def __aenter__(self):
        """Async context manager entry."""
        self.logger.debug("Entering async context")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        self.logger.debug("Exiting async context")
        await self.close()
