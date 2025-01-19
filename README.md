# UniFi Network Assistant

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)

A Python-based tool to interact with the UniFi Network Application API.

## Overview

This project uses the UniFi Network API to gather information about your UniFi network. It's built using Python and managed with `uv` package manager.

## UniFi Network API Capabilities

The UniFi Network API allows you to:

1. Device Management
   - List all devices in the network
   - Get detailed device information
   - Manage device settings
   - Perform device operations (restart, provision, etc.)

2. Network Configuration
   - View and manage networks
   - Configure VLANs
   - Manage port forwarding rules
   - Handle firewall rules

3. Client Management
   - List connected clients
   - View client statistics
   - Block/unblock clients
   - Manage client groups

4. Statistics and Monitoring
   - Get system statistics
   - Monitor network health
   - View bandwidth usage
   - Access event logs

## Authentication

The UniFi Network API uses API key authentication. You'll need to:
1. Generate an API key in your UniFi Network Application
2. Include it in the `X-API-KEY` header with each request
3. Use HTTPS for all API calls

Example API call:
```bash
curl -k -X GET 'https://192.168.1.1/proxy/network/integration/v1/sites' \
  -H 'X-API-KEY: YOUR_API_KEY' \
  -H 'Accept: application/json'
```

## Project Setup

### For Users
Once this package is published to PyPI, you can install it using:
```bash
uv tool install unifi-assist
```

### For Development
1. Clone the repository
2. Install dependencies:
```bash
uv sync
```

This will:
- Create a virtual environment if it doesn't exist
- Install all development and runtime dependencies
- Generate/update the lockfile

## Security Note

Never commit API keys to version control. We recommend using environment variables or a secure configuration file for storing sensitive credentials.

## Development Status

This project is currently in initial development. Documentation will be updated as features are implemented.

## Unifi Network API endpoints

UNIFI_HOST is set in `.env`.

UNIFI_HOST/integration/v1/sites/{siteId}/devices/{deviceId}/actions - POST
UNIFI_HOST/integration/v1/sites/{siteId}/devices - GET
UNIFI_HOST/integration/v1/sites/{siteId}/devices/{deviceId} - GET
UNIFI_HOST/integration/v1/sites/{siteId}/devices/{deviceId}/statistics/latest - GET
UNIFI_HOST/integration/v1/sites - GET
UNIFI_HOST/integration/v1/sites/{siteId}/clients - GET
UNIFI_HOST/integration/v1/info - GET

The official Unifi example uses this: https://unifi.ui.com/integration/v1/info.
This means that https:// may be required as well before UNIFI_HOST?
