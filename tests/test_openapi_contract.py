"""Every frozen public endpoint and parameter must work with both clients."""

import json

from scripts.check_openapi import DEFAULT_SCHEMA, check_contract


async def test_frozen_public_contract_has_no_sdk_gaps():
    spec = json.loads(DEFAULT_SCHEMA.read_text())
    operations = [
        operation
        for methods in spec["paths"].values()
        for verb, operation in methods.items()
        if verb in {"get", "post", "put", "patch", "delete"}
    ]
    parameters = [
        parameter
        for operation in operations
        for parameter in operation.get("parameters", [])
    ]
    expected_counts = {
        "operations": len(operations),
        "query_parameters": sum(p["in"] == "query" for p in parameters),
        "path_parameters": sum(p["in"] == "path" for p in parameters),
        "header_parameters": sum(p["in"] == "header" for p in parameters),
        "body_contracts": sum("requestBody" in operation for operation in operations),
    }
    results = await check_contract(spec)
    assert [result["client"] for result in results] == ["MalloryApi", "AsyncMalloryApi"]
    for result in results:
        assert not result["issues"], "\n".join(result["issues"])
        assert {key: result[key] for key in expected_counts} == expected_counts
