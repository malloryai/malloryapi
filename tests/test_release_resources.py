"""Response and upload behavior beyond the frozen route contracts."""

import json

import pytest

from malloryapi.exceptions import NotFoundError


async def test_sample_upload_preserves_bytes_and_length(sdk):
    upload = sdk.client.malware_samples.upload_content
    payload = b"\x00\xffsample\r\n"
    sdk.respond(status_code=202, json={"state": "uploaded"})
    result = await sdk.call(upload, "sample/one", payload)
    request = sdk.requests[0]
    assert result == {"state": "uploaded"}
    assert request.content == payload
    assert request.headers["content-type"] == "application/octet-stream"
    assert request.headers["content-length"] == str(len(payload))
    assert request.url.raw_path == b"/v1/malware-samples/sample%2Fone/content"


@pytest.mark.parametrize("method", ["create", "analyze"])
async def test_sample_idempotency_is_a_header(sdk, method):
    fn = getattr(sdk.client.malware_samples, method)
    data = (
        {"integration_uuids": None}
        if method == "analyze"
        else {"original_filename": "sample.bin", "expected_size_bytes": 7}
    )
    args = ("sample-one", data) if method == "analyze" else (data,)
    sdk.respond(json={"uuid": "result-one"})
    await sdk.call(fn, *args, idempotency_key="same-logical-request")
    request = sdk.requests[0]
    assert request.headers["idempotency-key"] == "same-logical-request"
    assert not request.url.query
    assert json.loads(request.content) == data


@pytest.mark.parametrize(
    "resource,method,args,content_type",
    [
        ("detections", "download", ("detection-one",), "application/zip"),
        (
            "malware_sample_reports",
            "artifact",
            ("report-one", "report.json"),
            "application/json",
        ),
        (
            "malware_sample_reports",
            "artifact",
            ("report-one", "trace.bin"),
            "application/octet-stream",
        ),
    ],
)
async def test_downloads_preserve_exact_bytes(
    sdk, resource, method, args, content_type
):
    fn = getattr(getattr(sdk.client, resource), method)
    payload = (
        b'{"value":  0}\n' if content_type == "application/json" else b"PK\x00\xff"
    )
    sdk.respond(content=payload, headers={"content-type": content_type})
    assert await sdk.call(fn, *args) == payload


async def test_binary_download_errors_remain_api_errors(sdk):
    fn = sdk.client.detections.download
    sdk.respond(status_code=404, json={"detail": "Not found"})
    with pytest.raises(NotFoundError) as error:
        await sdk.call(fn, "missing")
    assert error.value.response_body == {"detail": "Not found"}


async def test_package_search_preserves_both_pages_and_resolution(sdk):
    search = sdk.client.packages.search
    response = {
        "resolution": {"status": "resolved"},
        "normalized_request": {"ecosystem": "npm", "name": "example", "version": "1.0"},
        "coverage": {"evaluation_complete": False},
        "vulnerabilities": {"data": [{"cve_id": "CVE-2026-1234"}], "offset": 0},
        "compromises": {"data": [{"uuid": "compromise-one"}], "offset": 5},
    }
    sdk.respond(json=response)
    result = await sdk.call(
        search,
        {"purl": "pkg:npm/example@1.0"},
        vulnerability_offset=0,
        compromise_offset=5,
        limit=10,
    )
    assert result == response
    assert dict(sdk.requests[0].url.params) == {
        "vulnerability_offset": "0",
        "compromise_offset": "5",
        "limit": "10",
    }


async def test_detection_revisions_preserve_pagination(sdk):
    fn = sdk.client.detections.revisions
    sdk.respond(
        json={"data": [{"uuid": "revision-one"}], "total": 4, "offset": 0, "limit": 1}
    )
    result = await sdk.call(fn, "detection-one", limit=1)
    assert result.items == [{"uuid": "revision-one"}]
    assert result.total == 4
    assert result.has_more


@pytest.mark.parametrize("status", [302, 307])
async def test_binary_redirect_is_not_returned_as_a_download(sdk, status):
    from malloryapi.exceptions import APIError

    sdk.respond(status_code=status, headers={"Location": "https://example.test/file"})
    with pytest.raises(APIError) as error:
        await sdk.call(sdk.client.detections.download, "one")
    assert error.value.status_code == status
