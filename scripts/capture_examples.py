#!/usr/bin/env python3
"""
Script to capture example responses from the UniFi Network API.
This helps validate our API spec and provides test fixtures.
"""

import asyncio
import json
import logging
import os
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path

from unifi_assist.client import UniFiClient

# Set up logging like in test.py
logging.basicConfig(level=logging.DEBUG)

EXAMPLES_DIR = Path(__file__).parent.parent / "examples"
API_RESPONSES_DIR = EXAMPLES_DIR / "api_responses"


def save_response(name: str, data: dict, site: str = None):
    """Save API response to a JSON file with metadata."""
    timestamp = datetime.now().isoformat()

    # Add metadata to help track the response
    response_with_metadata = {
        "captured_at": timestamp,
        "site": site,
        "endpoint": name,
        "response": data,
    }

    # Create filename with timestamp for uniqueness
    filename = f"{name}_{timestamp.replace(':', '-')}.json"
    if site:
        filename = f"{site}_{filename}"

    filepath = API_RESPONSES_DIR / filename

    with open(filepath, "w") as f:
        json.dump(response_with_metadata, f, indent=2)

    print(f"Saved response to {filepath}")


async def capture_responses(client: UniFiClient):
    """Capture responses from various UniFi API endpoints."""
    # Get list of sites
    sites_response = await client.get_sites()
    save_response("sites", sites_response)

    # Extract sites from response
    sites = sites_response.get("data", [])
    if not sites:
        print("No sites found")
        return

    # Get system info
    info = await client.get_system_info()
    save_response("info", info)

    # For each site, get devices and clients
    for site in sites:
        site_id = site.get("id")
        if not site_id:
            print("Site missing ID, skipping")
            continue

        print(f"\nProcessing site {site_id}")

        # Get devices
        devices_response = await client.get_devices(site_id)
        save_response("devices", devices_response, site_id)

        # Extract devices from response
        devices = devices_response.get("data", [])

        # Get clients
        clients = await client.get_clients(site_id)
        save_response("clients", clients, site_id)

        # For each device, get details and statistics
        if devices:
            for device in devices:
                device_id = device.get("id")
                if not device_id:
                    print("Device missing ID, skipping")
                    continue

                print(f"Getting details for device {device_id}")

                # Get device details
                device_details = await client.get_device_details(site_id, device_id)
                save_response(f"device_details_{device_id}", device_details, site_id)

                # Get device statistics
                device_stats = await client.get_device_statistics(site_id, device_id)
                save_response(f"device_stats_{device_id}", device_stats, site_id)


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
    async with UniFiClient(host=host, api_key=api_key, verify_ssl=False) as client:
        await capture_responses(client)
        print("\nAPI response capture complete!")


if __name__ == "__main__":
    asyncio.run(main())
