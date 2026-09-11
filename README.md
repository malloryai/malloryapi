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

### Platform and investigation

| Resource | Accessor | Use |
| --- | --- | --- |
| Findings and tickets | `client.findings` | Findings, bulk updates, ticket connections and linked findings |
| Finding definitions | `client.finding_definitions` | List, create, get, update and delete definitions |
| Profiles | `client.profiles` | Profile CRUD, entities and topics |
| Sightings | `client.sightings` | List, create and bulk-create sightings |
| Assets | `client.assets` | Live catalog, match summaries and matched-asset queries |
| Observables | `client.observables` | Observable CRUD, entities, opinions, tags and enrichment-provider metadata |
| CVE inference | `client.vulnerable_configurations`, `client.vtpcs` | Product/version inference using either API route |

The SDK exposes all 252 operations in the public OpenAPI snapshot captured on
September 11, 2026, in both sync and async clients. Existing methods for routes
omitted from the public schema remain available for compatibility.

### Query parameters and request bodies

Methods accept documented filters as named keyword arguments, including through
`**kwargs` where the filter set is large. Query values of `None` are omitted;
`False`, `0` and lists are preserved. JSON request bodies keep explicit `null`
values. Dictionary bodies follow the API schema and are validated by the server.

```python
products = client.products.search(
    {"vendor": "apache", "product": "http_server"},
    offset=0, limit=20, sort="name", order="asc",
)
client.references.create(
    ["https://example.com/report"], submitter="my-integration"
)
findings = client.findings.list(limit=20)
matches = client.assets.list_matches(limit=20)
```

### CVE inference

Both inference resources return `InferenceResponse`, which keeps the existing
pagination interface and exposes `resolution`, `normalized_request`, `mode` and
`coverage`. Inspect identity resolution and coverage when interpreting results.

```python
result = client.vtpcs.search(
    {"vendor": "apache", "product": "http_server", "version": "2.4.49"},
    limit=50, include_unknown=True,
)
print(result.resolution, result.coverage)
for vulnerability in result:
    print(vulnerability)
```

## Pagination

Paginated list methods return a `PaginatedResponse` with `.items`, `.total`,
`.offset`, `.limit`, and `.has_more`. Additional envelope fields are preserved in
`.metadata`. Methods with specialized response envelopes, such as asset matches,
return the API dictionary directly.

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

Auto-pagination requires a positive `limit` and stops on an empty page or the
last page reported by the API.

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

Successful operations with an empty `204 No Content` response return `None`.

## CLI

Use `malloryapi --help-resources` to discover resources and methods. Supply
additional keyword arguments with repeatable `--param NAME=VALUE` options;
JSON booleans, numbers, lists and objects keep their types.

```bash
malloryapi findings list --limit 20
malloryapi stories get STORY_UUID --param include_proto=true
malloryapi products search '{"vendor":"apache","product":"http_server"}' --limit 20
malloryapi references create --urls https://example.com/report --param submitter=my-integration
```

## Development and contract checks

```bash
python -m pytest -q
python -m ruff check src/ tests/ scripts/
python scripts/check_openapi.py
# Compare with a separately downloaded current schema:
python scripts/check_openapi.py --schema /path/to/openapi.json
```

The contract check uses an HTTP mock transport, so it sends no API requests.
It checks every public method/path, path substitution, query parameter and JSON
body field in both clients. Regression tests also cover response envelopes and
no-content success. The frozen fixture excludes descriptive documentation but
retains operation and schema contracts. Passing checks establish SDK transport
coverage; they do not exercise authorization or server-side business validation.

### Test structure

- `test_openapi_contract.py` checks the frozen public schema against both clients.
  Update the fixture when the API contract changes; avoid copying its endpoint
  and parameter tables into individual tests.
- Focused regression tests cover behavior beyond route forwarding: response
  envelopes, pagination, errors, CLI arguments, legacy routes, and the difference
  between omitted values and JSON `null`.
- `test_contract_checker.py` injects deliberately broken implementations to prove
  the contract checker detects missing routes and corrupted parameters or bodies.

Use the shared `sdk` fixture for resource and HTTP tests. Each test runs against
both sync and async clients through a real HTTPX client with an in-memory
transport. Configure one response per expected request; unexpected additional
requests fail. The fixture closes the client automatically.

```python
async def test_empty_success(sdk):
    sdk.respond(status_code=204)

    result = await sdk.call(sdk.client.workspaces.delete, "workspace-1")

    assert result is None
    assert sdk.requests[0].method == "DELETE"
```

Both public clients accept a keyword-only `transport=` dependency:
`httpx.BaseTransport` for `MalloryApi` and `httpx.AsyncBaseTransport` for
`AsyncMalloryApi`. `httpx.MockTransport` supports both. The SDK owns its HTTPX
client and closes the supplied transport when the SDK is closed; use a context
manager or call `close()` / `aclose()`. Tests should inject this dependency instead
of replacing private client attributes. CLI tests similarly call
`main(argv, transport=...)` and capture output with pytest's `capsys` fixture.

## License

Apache 2.0
