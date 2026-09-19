"""The CLI preserves binary uploads and downloads."""

import httpx
import pytest

from malloryapi.cli import main


def test_download_to_file(tmp_path, capsys):
    target = tmp_path / "rules.zip"
    payload = b"PK\x00\xff"
    transport = httpx.MockTransport(lambda r: httpx.Response(200, content=payload))
    code = main(
        [
            "--api-key",
            "test-key",
            "detections",
            "download",
            "one",
            "--output",
            str(target),
        ],
        transport=transport,
    )
    assert code == 0
    assert target.read_bytes() == payload
    assert capsys.readouterr().out == ""


def test_upload_from_file(tmp_path, capsys):
    source = tmp_path / "sample.bin"
    payload = b"\x00\xffsample"
    source.write_bytes(payload)
    requests = []

    def respond(request):
        requests.append(request)
        return httpx.Response(202, json={"state": "uploaded"})

    code = main(
        [
            "--api-key",
            "test-key",
            "malware_samples",
            "upload_content",
            "one",
            "--input-file",
            str(source),
        ],
        transport=httpx.MockTransport(respond),
    )
    assert code == 0
    assert requests[0].content == payload
    assert '"state": "uploaded"' in capsys.readouterr().out


def test_binary_result_requires_output_path(capsys):
    transport = httpx.MockTransport(lambda r: httpx.Response(200, content=b"PK"))
    code = main(
        ["--api-key", "test-key", "detections", "download", "one"], transport=transport
    )
    output = capsys.readouterr()
    assert code == 1
    assert not output.out
    assert "--output" in output.err


@pytest.mark.parametrize(
    "args",
    [
        ["detections", "list"],
        ["malware_samples", "upload_content", "one", "--param", "content=already"],
    ],
)
def test_incompatible_file_input_fails_before_request(tmp_path, capsys, args):
    source = tmp_path / "sample.bin"
    source.write_bytes(b"sample")
    requests = []

    def respond(request):
        requests.append(request)
        return httpx.Response(200, json={})

    code = main(
        ["--api-key", "test-key", *args, "--input-file", str(source)],
        transport=httpx.MockTransport(respond),
    )
    assert code == 1
    assert requests == []
    assert "--input-file" in capsys.readouterr().err


def test_invalid_output_option_prevents_mutation(tmp_path, capsys):
    requests = []

    def respond(request):
        requests.append(request)
        return httpx.Response(204)

    code = main(
        [
            "--api-key",
            "test-key",
            "malware_samples",
            "delete",
            "sample-one",
            "--output",
            str(tmp_path / "unexpected.bin"),
        ],
        transport=httpx.MockTransport(respond),
    )
    assert code == 1
    assert requests == []
    assert "--output" in capsys.readouterr().err
