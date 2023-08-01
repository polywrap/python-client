from typing import Callable
from polywrap_client import PolywrapClient
from polywrap_core import Uri
from eth_account.signers.local import LocalAccount

WithSigner = bool
provider_uri = Uri.from_str("plugin/ethereum-provider")

def test_signer_address(client_factory: Callable[[WithSigner], PolywrapClient], account: LocalAccount):
    client = client_factory(True)
    result = client.invoke(
        uri=provider_uri,
        method="signerAddress",
        args={},
        encode_result=False
    )

    assert result == account.address  # type: ignore

def test_signer_address_no_signer(client_factory: Callable[[WithSigner], PolywrapClient]):
    client = client_factory(False)
    result = client.invoke(
        uri=provider_uri,
        method="signerAddress",
        args={},
        encode_result=False
    )

    assert result is None
