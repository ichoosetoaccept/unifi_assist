from typing import Optional, List, Dict, Any
import httpx
from pydantic import BaseModel
from pathlib import Path
import os
from dotenv import load_dotenv

class UniFiClient:
    def __init__(
        self,
        host: str,
        api_key: Optional[str] = None,
        verify_ssl: bool = True
    ):
        """Initialize UniFi API client.
        
        Args:
            host: UniFi controller hostname/IP (e.g., '192.168.1.1')
            api_key: API key for authentication
            verify_ssl: Whether to verify SSL certificates
        """
        self.base_url = f"https://{host}"
        self.api_key = api_key or os.getenv("UNIFI_API_KEY")
        if not self.api_key:
            raise ValueError("API key must be provided or set in UNIFI_API_KEY environment variable")
        
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            verify=verify_ssl,
            headers={
                "Accept": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
        )
    
    async def get_sites(self) -> List[Dict[str, Any]]:
        """Get all available sites."""
        response = await self.client.get("/proxy/network/integration/v1/sites")
        response.raise_for_status()
        return response.json()
    
    async def get_device_stats(self, site: str) -> List[Dict[str, Any]]:
        """Get device statistics for a site."""
        response = await self.client.get(f"/proxy/network/api/s/{site}/stat/device")
        response.raise_for_status()
        return response.json().get("data", [])
    
    async def get_client_stats(self, site: str) -> List[Dict[str, Any]]:
        """Get client statistics for a site."""
        response = await self.client.get(f"/proxy/network/api/s/{site}/stat/sta")
        response.raise_for_status()
        return response.json().get("data", [])
    
    async def get_network_health(self, site: str) -> Dict[str, Any]:
        """Get network health statistics."""
        response = await self.client.get(f"/proxy/network/api/s/{site}/stat/health")
        response.raise_for_status()
        return response.json().get("data", {})
    
    async def get_system_info(self, site: str) -> Dict[str, Any]:
        """Get system information."""
        response = await self.client.get(f"/proxy/network/api/s/{site}/stat/sysinfo")
        response.raise_for_status()
        return response.json().get("data", {})
    
    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()