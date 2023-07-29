from pathlib import Path
from polywrap_client_config_builder import PolywrapClientConfigBuilder
from polywrap_core import Uri, UriResolutionContext
from polywrap_client import PolywrapClient
from polywrap_sys_config_bundle import get_sys_config


def test_http_plugin():
    config = PolywrapClientConfigBuilder().add(get_sys_config()).build()
    client = PolywrapClient(config)

    response = client.invoke(
        uri=Uri.from_str("ens/wraps.eth:http@1.1.0"),
        method="get",
        args={"url": "https://www.google.com"},
    )

    assert response["status"] == 200
    assert response["body"] is not None


def test_file_system_resolver():
    config = PolywrapClientConfigBuilder().add(get_sys_config()).build()
    client = PolywrapClient(config)

    path_to_resolve = str(Path(__file__).parent.parent / "polywrap_sys_config_bundle" / "embeds" / "http-resolver")

    response = client.invoke(
        uri=Uri.from_str("ens/wraps.eth:file-system-uri-resolver-ext@1.0.1"),
        method="tryResolveUri",
        args={"authority": "fs", "path": path_to_resolve},
    )

    assert response["manifest"]


def test_http_resolver():
    config = PolywrapClientConfigBuilder().add(get_sys_config()).build()
    client = PolywrapClient(config)

    response = client.invoke(
        uri=Uri.from_str("ens/wraps.eth:http-uri-resolver-ext@1.0.1"),
        method="tryResolveUri",
        args={"authority": "https", "path": "wraps.wrapscan.io/r/polywrap/wrapscan-uri-resolver@1.0"},
    )

    assert response["uri"]
    assert Uri.from_str(response["uri"]).authority == "ipfs"


def test_resolve_wrapscan_resolver():
    config = PolywrapClientConfigBuilder().add(get_sys_config()).build()
    client = PolywrapClient(config)
    response = client.try_resolve_uri(
        Uri("wrapscan.io", "polywrap/wrapscan-uri-resolver@1.0"),
    )

    assert response
    assert isinstance(response, Uri)
    assert response.authority == "ipfs"
