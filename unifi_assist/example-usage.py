import asyncio
from unifi_assist.client import UniFiClient
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

async def main():
    # Client will automatically use UNIFI_HOST and UNIFI_API_KEY from environment
    async with UniFiClient(verify_ssl=False) as client:
        # Get all sites
        sites = await client.get_sites()
        
        # Use the first site for our examples
        if sites:
            site_id = sites[0]["id"]
            
            # Get various statistics
            devices = await client.get_device_stats(site_id)
            clients = await client.get_client_stats(site_id)
            health = await client.get_network_health(site_id)
            sysinfo = await client.get_system_info(site_id)
            
            # Print some interesting information
            print(f"\nSystem Information:")
            print(f"Version: {sysinfo.get('version', 'Unknown')}")
            
            print(f"\nNetwork Health:")
            for subsystem in health:
                print(f"{subsystem['subsystem']}: {subsystem['status']}")
            
            print(f"\nDevice Summary:")
            print(f"Total Devices: {len(devices)}")
            
            print(f"\nClient Summary:")
            print(f"Total Clients: {len(clients)}")

if __name__ == "__main__":
    asyncio.run(main())