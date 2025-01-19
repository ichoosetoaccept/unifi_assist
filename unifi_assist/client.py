from typing import Optional, List, Dict, Any
import aiohttp
import ssl
from pydantic import BaseModel
from pathlib import Path
import os
from dotenv import load_dotenv
from .logging import setup_logging

# Load environment variables
load_dotenv()

class UniFiClient:
    def __init__(
        self,
        host: Optional[str] = None,
        api_key: Optional[str] = None,
        verify_ssl: bool = True
    ):
        """Initialize UniFi API client.
        
        Args:
            host: UniFi controller hostname/IP (defaults to UNIFI_HOST env var)
            api_key: API key for authentication (defaults to UNIFI_API_KEY env var)
            verify_ssl: Whether to verify SSL certificates
        """
        self.logger = setup_logging("unifi_client")
        self.host = host or os.getenv("UNIFI_HOST")
        if not self.host:
            raise ValueError("Host must be provided or set in UNIFI_HOST environment variable")
            
        self.base_url = f"https://{self.host}"
        self.api_key = api_key or os.getenv("UNIFI_API_KEY")
        if not self.api_key:
            raise ValueError("API key must be provided or set in UNIFI_API_KEY environment variable")
        
        self.logger.info(f"Initializing UniFi client for host: {self.host}")
        
        # SSL context setup
        if verify_ssl:
            self.ssl_context = True  # aiohttp will use default SSL context
        else:
            self.ssl_context = ssl.create_default_context()
            self.ssl_context.check_hostname = False
            self.ssl_context.verify_mode = ssl.CERT_NONE
            
        # Session will be initialized in __aenter__ or when first needed
        self.client = None
        self._session_headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
    
    async def _ensure_client(self):
        """Ensure client session exists."""
        if self.client is None:
            self.client = aiohttp.ClientSession(
                base_url=self.base_url,
                headers=self._session_headers
            )
        return self.client
    
    async def get_sites(self) -> List[Dict[str, Any]]:
        """Get all available sites."""
        self.logger.debug("Fetching available sites")
        client = await self._ensure_client()
        async with client.get("/proxy/network/integration/v1/sites", ssl=self.ssl_context) as response:
            await response.raise_for_status()
            sites = await response.json()
            self.logger.info(f"Found {len(sites)} sites")
            return sites
    
    async def get_device_stats(self, site: str) -> List[Dict[str, Any]]:
        """Get device statistics for a site."""
        self.logger.debug(f"Fetching device stats for site: {site}")
        client = await self._ensure_client()
        async with client.get(f"/proxy/network/api/s/{site}/stat/device", ssl=self.ssl_context) as response:
            await response.raise_for_status()
            data = await response.json()
            stats = data.get("data", [])
            self.logger.info(f"Found stats for {len(stats)} devices in site {site}")
            return stats
    
    async def get_client_stats(self, site: str) -> List[Dict[str, Any]]:
        """Get client statistics for a site."""
        self.logger.debug(f"Fetching client stats for site: {site}")
        client = await self._ensure_client()
        async with client.get(f"/proxy/network/api/s/{site}/stat/sta", ssl=self.ssl_context) as response:
            await response.raise_for_status()
            data = await response.json()
            stats = data.get("data", [])
            self.logger.info(f"Found stats for {len(stats)} clients in site {site}")
            return stats
    
    async def get_network_health(self, site: str) -> Dict[str, Any]:
        """Get network health statistics."""
        self.logger.debug(f"Fetching network health for site: {site}")
        client = await self._ensure_client()
        async with client.get(f"/proxy/network/api/s/{site}/stat/health", ssl=self.ssl_context) as response:
            await response.raise_for_status()
            data = await response.json()
            health = data.get("data", {})
            self.logger.info(f"Retrieved network health data for site {site}")
            return health
    
    async def get_system_info(self, site: str) -> Dict[str, Any]:
        """Get system information."""
        self.logger.debug(f"Fetching system info for site: {site}")
        client = await self._ensure_client()
        async with client.get(f"/proxy/network/api/s/{site}/stat/sysinfo", ssl=self.ssl_context) as response:
            await response.raise_for_status()
            data = await response.json()
            info = data.get("data", {})
            self.logger.info(f"Retrieved system info for site {site}")
            return info
    
    async def close(self):
        """Close the HTTP client."""
        if self.client:
            self.logger.debug("Closing HTTP client")
            await self.client.close()
            self.client = None
    
    async def __aenter__(self):
        await self._ensure_client()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()