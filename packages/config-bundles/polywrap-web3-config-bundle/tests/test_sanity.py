from polywrap_client_config_builder import PolywrapClientConfigBuilder
from polywrap_core import Uri, UriPackage
from polywrap_client import PolywrapClient
from polywrap_web3_config_bundle import get_web3_config


def test_ens_content_hash_resolver():
    config = PolywrapClientConfigBuilder().add(get_web3_config()).build()
    client = PolywrapClient(config)

    result = client.try_resolve_uri(
        uri=Uri.from_str("wrap://ens/wrap-link.eth")
    )

    assert result is not None
    assert isinstance(result, UriPackage)
