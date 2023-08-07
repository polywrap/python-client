from polywrap_client_config_builder import PolywrapClientConfigBuilder
from polywrap_core import Uri, UriPackage
from polywrap_client import PolywrapClient
from polywrap_web3_config_bundle import web3_bundle
from polywrap_sys_config_bundle import sys_bundle


def test_ens_content_hash_resolver():
    config = PolywrapClientConfigBuilder().add_bundle(web3_bundle).build()
    client = PolywrapClient(config)

    result = client.try_resolve_uri(
        uri=Uri.from_str("wrap://ens/wrap-link.eth")
    )

    assert result is not None
    assert isinstance(result, UriPackage)


def test_sys_web3_config_bundle():
    builder = PolywrapClientConfigBuilder().add_bundle(sys_bundle).add_bundle(web3_bundle)

    client = PolywrapClient(builder.build())

    result = client.invoke(
        uri=Uri.from_str('wrapscan.io/polywrap/ipfs-http-client'),
        method="cat",
        args={
            "cid": "QmZ4d7KWCtH3xfWFwcdRXEkjZJdYNwonrCwUckGF1gRAH9",
            "ipfsProvider": "https://ipfs.io",
        },
        encode_result=False
    )

    print(result)
    assert result.startswith(b"<svg")