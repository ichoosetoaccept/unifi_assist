import asyncio
from unifi_assist.client import UniFiClient

async def main():
    async with UniFiClient(host="192.168.1.1", api_key="your-api-key") as client:
        # Get all sites
        sites = await client.get_sites()
        print("Available sites:", sites)
        
        # Get device stats for the default site
        devices = await client.get_device_stats("default")
        print("Device stats:", devices)
        
        # Get network health
        health = await client.get_network_health("default")
        print("Network health:", health)

if __name__ == "__main__":
    asyncio.run(main())