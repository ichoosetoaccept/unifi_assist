# UniFi Network Assistant

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/140cf4020fd64f4c9fcc3f52d84b03a8)](https://app.codacy.com/gh/ichoosetoaccept/unifi_assist/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)

A Python-based tool to interact with the UniFi Network Application API.

## Overview

This project uses the UniFi Network API to gather information about your UniFi
network. It's built using Python and managed with `uv` package manager.

## UniFi Network API Capabilities

The UniFi Network API provides comprehensive network management capabilities:

| Category | Capabilities | Example Endpoints |
|----------|--------------|------------------|
| Device Management | • List all devices • Get device details • Manage settings • Perform operations (restart, provision) | `GET /proxy/network/integration/v1/sites/{site}/devices` • `GET /proxy/network/integration/v1/sites/{site}/devices/{id}` • `POST /proxy/network/integration/v1/sites/{site}/devices/{id}/actions` |
| Network Configuration | • View/manage networks • Configure VLANs • Manage port forwarding • Handle firewall rules | `GET /proxy/network/integration/v1/sites/{site}/settings` • `GET /proxy/network/integration/v1/sites/{site}/vlans` • `POST /proxy/network/integration/v1/sites/{site}/settings` |
| Client Management | • List connected clients • View client statistics • Block/unblock clients • Manage client groups | `GET /proxy/network/integration/v1/sites/{site}/clients` • `GET /proxy/network/integration/v1/sites/{site}/client/{mac}` • `POST /proxy/network/integration/v1/sites/{site}/client/{mac}/block` |
| Statistics & Monitoring | • System statistics • Network health • Bandwidth usage • Event logs | `GET /proxy/network/integration/v1/sites/{site}/health` • `GET /proxy/network/integration/v1/sites/{site}/stats` • `GET /proxy/network/integration/v1/sites/{site}/devices/{id}/statistics/latest` |

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

### Commit Message Guidelines

This project follows [Conventional Commits](https://www.conventionalcommits.org/) specification. Each commit message should be structured as follows:

```text
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

Types:

- `feat`: A new feature (minor version bump)
- `fix`: A bug fix (patch version bump)
- `docs`: Documentation only changes
- `style`: Changes that don't affect code meaning
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `perf`: Code change that improves performance
- `test`: Adding missing tests or correcting existing tests
- `chore`: Changes to build process or auxiliary tools

Examples:

```text
feat(api): add device status endpoint
fix: correct token refresh logic
docs: update API authentication guide
test(client): add test for error handling
```

Breaking Changes:
For commits that break backward compatibility, add `BREAKING CHANGE:` in the footer or append a `!` after the type:

```text
feat!: remove deprecated login method

BREAKING CHANGE: The `login` method has been removed. Use `authenticate` instead.
```

## Security Note

Never commit API keys to version control. We recommend using environment
variables or a secure configuration file for storing sensitive credentials.

## Development Status

This project is currently in initial development. Documentation will be updated
as features are implemented.
