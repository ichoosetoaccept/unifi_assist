import asyncio
import os
from dotenv import load_dotenv
from unifi_assist.client import UniFiClient
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)


async def main():
    # Load environment variables
    load_dotenv()

    # Get credentials from environment
    host = os.getenv("UNIFI_HOST")
    api_key = os.getenv("UNIFI_API_KEY")

    if not host or not api_key:
        print("Error: UNIFI_HOST and UNIFI_API_KEY must be set in environment")
        return

    print(f"Using host: {host}")
    print(f"Using API key: {api_key}")

    # Create client instance and use it as context manager
    async with UniFiClient(host, api_key, verify_ssl=False) as client:
        # Try to get sites
        print("\nAttempting to get sites...")
        sites = await client.get_sites()
        print("Success! Sites:", sites)


if __name__ == "__main__":
    asyncio.run(main())
