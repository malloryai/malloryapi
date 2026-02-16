# malloryapi

Official Python client for the [Mallory](https://mallory.ai) threat intelligence API.

## Installation

```bash
pip install malloryapi
# or
uv add malloryapi
```

## Quick Start

```python
from malloryapi import MalloryApi

client = MalloryApi(api_key="your-api-key")

# List recent vulnerabilities
vulns = client.vulnerabilities.list(limit=10)
for v in vulns:
    print(v["cve_id"], v.get("cvss_base_score"))

# Get a specific vulnerability
vuln = client.vulnerabilities.get("CVE-2024-1234")

# Trending threat actors (last 7 days)
actors = client.threat_actors.trending(period="7d")
```

## Authentication

Pass your API key directly or set the `MALLORY_API_KEY` environment variable:

```python
# Explicit
client = MalloryApi(api_key="sk-...")

# From environment
import os
os.environ["MALLORY_API_KEY"] = "sk-..."
client = MalloryApi()
```

## Async Support

```python
from malloryapi import AsyncMalloryApi

async with AsyncMalloryApi(api_key="sk-...") as client:
    vulns = await client.vulnerabilities.list(limit=10)
    actor = await client.threat_actors.get("apt28-uuid")
```

## Resources

### Entities

| Resource             | Accessor                      | Key Methods                                                                                          |
| -------------------- | ----------------------------- | ---------------------------------------------------------------------------------------------------- |
| Vulnerabilities      | `client.vulnerabilities`      | `list`, `get`, `trending`, `exploited`, `export`, `exploits`, `mentions`, `products`, `observables`  |
| Threat Actors        | `client.threat_actors`        | `list`, `get`, `trending`, `export`, `mentions`, `observables`, `attack_patterns`                    |
| Malware              | `client.malware`              | `list`, `get`, `trending`, `export`, `mentions`, `observables`, `vulnerabilities`, `attack_patterns` |
| Exploits             | `client.exploits`             | `list`, `get`, `export`, `vulnerabilities`                                                           |
| Exploitations        | `client.exploitations`        | `list`, `get`                                                                                        |
| Organizations        | `client.organizations`        | `list`, `get`, `trending`, `export`, `mentions`, `products`, `breaches`                              |
| Products             | `client.products`             | `list`, `get`, `trending`, `search`, `export`, `advisories`, `mentions`                              |
| Attack Patterns      | `client.attack_patterns`      | `list`, `get`, `trending`, `mentions`, `threat_actors`, `malware`                                    |
| Breaches             | `client.breaches`             | `list`, `get`, `organizations`                                                                       |
| Detection Signatures | `client.detection_signatures` | `list`, `get`                                                                                        |
| Advisories           | `client.advisories`           | `list`, `get`, `export`, `products`, `vulnerabilities`                                               |
| Weaknesses           | `client.weaknesses`           | `list`, `get`                                                                                        |

### Content

| Resource       | Accessor                | Key Methods                                                                       |
| -------------- | ----------------------- | --------------------------------------------------------------------------------- |
| Stories        | `client.stories`        | `list`, `get`, `topics`, `references`, `events`, `similar`, `entities`, `export`  |
| References     | `client.references`     | `list`, `get`, `create`, `labels`, `entities`, `threat_actors`, `vulnerabilities` |
| Sources        | `client.sources`        | `list`, `statistics`                                                              |
| Content Chunks | `client.content_chunks` | `list`, `get`, `search`                                                           |

### Analytics

| Resource | Accessor          | Key Methods                         |
| -------- | ----------------- | ----------------------------------- |
| Mentions | `client.mentions` | `list`, `actors`, `vulnerabilities` |
| Search   | `client.search`   | `query`                             |

## Pagination

All list methods return a `PaginatedResponse` with `.items`, `.total`, `.offset`, `.limit`, and `.has_more`:

```python
page = client.vulnerabilities.list(offset=0, limit=50)
print(f"Showing {len(page)} of {page.total}")

if page.has_more:
    next_page = client.vulnerabilities.list(offset=50, limit=50)
```

### Auto-pagination

Iterate over all results automatically:

```python
from malloryapi import paginate_sync

for vuln in paginate_sync(client.vulnerabilities.list, limit=100):
    print(vuln["cve_id"])
```

Async version:

```python
from malloryapi import paginate_async

async for vuln in paginate_async(client.vulnerabilities.list):
    print(vuln["cve_id"])
```

## Trending

Entities with trending support accept a `period` parameter (`"1d"`, `"7d"`, or `"30d"`):

```python
# Trending vulnerabilities over the last 30 days
vulns = client.vulnerabilities.trending(period="30d")

# Trending threat actors (defaults to 7 days)
actors = client.threat_actors.trending()
```

## Error Handling

```python
from malloryapi import MalloryApi, NotFoundError, AuthenticationError

client = MalloryApi(api_key="sk-...")

try:
    vuln = client.vulnerabilities.get("CVE-9999-0000")
except NotFoundError:
    print("Vulnerability not found")
except AuthenticationError:
    print("Invalid API key")
```

All exceptions inherit from `APIError` and include `status_code` and `response_body` attributes.

## License

Apache 2.0
