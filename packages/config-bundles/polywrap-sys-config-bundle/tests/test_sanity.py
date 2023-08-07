from pathlib import Path
from polywrap_client_config_builder import PolywrapClientConfigBuilder
from polywrap_core import Uri, UriPackage
from polywrap_client import PolywrapClient
from polywrap_sys_config_bundle import sys_bundle


def test_http_plugin():
    config = PolywrapClientConfigBuilder().add_bundle(sys_bundle).build()
    client = PolywrapClient(config)

    response = client.invoke(
        uri=Uri.from_str("ens/wraps.eth:http@1.1.0"),
        method="get",
        args={"url": "https://www.google.com"},
    )

    assert response["status"] == 200
    assert response["body"] is not None


def test_file_system_resolver():
    config = PolywrapClientConfigBuilder().add_bundle(sys_bundle).build()
    client = PolywrapClient(config)

    path_to_resolve = str(Path(__file__).parent.parent / "polywrap_sys_config_bundle" / "embeds" / "http-resolver")

    response = client.invoke(
        uri=Uri.from_str("ens/wraps.eth:file-system-uri-resolver-ext@1.0.1"),
        method="tryResolveUri",
        args={"authority": "fs", "path": path_to_resolve},
    )

    assert response["manifest"]

    uri_package = client.try_resolve_uri(
        uri=Uri.from_str(f"wrap://fs/{path_to_resolve}")
    )
    assert uri_package
    assert isinstance(uri_package, UriPackage)


def test_http_resolver():
    config = PolywrapClientConfigBuilder().add_bundle(sys_bundle).build()
    client = PolywrapClient(config)
    http_path = "wraps.wrapscan.io/r/polywrap/wrapscan-uri-resolver@1.0"

    response = client.invoke(
        uri=Uri.from_str("ens/wraps.eth:http-uri-resolver-ext@1.0.1"),
        method="tryResolveUri",
        args={"authority": "https", "path": http_path},
    )

    assert response["uri"]
    assert Uri.from_str(response["uri"]).authority == "ipfs"

    uri_package = client.try_resolve_uri(
        uri=Uri.from_str(f"wrap://https/{http_path}")
    )
    assert uri_package
    assert isinstance(uri_package, UriPackage)



def test_ipfs_resolver():
    config = PolywrapClientConfigBuilder().add_bundle(sys_bundle).build()
    client = PolywrapClient(config)

    result = client.try_resolve_uri(
        uri=Uri.from_str("wrap://ipfs/QmfRCVA1MSAjUbrXXjya4xA9QHkbWeiKRsT7Um1cvrR7FY")
    )

    assert result is not None
    assert isinstance(result, UriPackage)


def test_can_resolve_wrapscan_resolver():
    config = PolywrapClientConfigBuilder().add_bundle(sys_bundle).build()
    client = PolywrapClient(config)
    response = client.try_resolve_uri(
        Uri("wrapscan.io", "polywrap/wrapscan-uri-resolver@1.0"),
    )

    assert response
    assert isinstance(response, UriPackage)


def test_wrapscan_resolver():
    config = PolywrapClientConfigBuilder().add_bundle(sys_bundle).build()
    client = PolywrapClient(config)
    response = client.try_resolve_uri(
        Uri("wrapscan.io", "polywrap/uri-resolver@1.0"),
    )

    assert response
    assert isinstance(response, UriPackage)
