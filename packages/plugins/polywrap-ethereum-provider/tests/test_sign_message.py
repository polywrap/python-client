from typing import Callable
from polywrap_client import PolywrapClient
from polywrap_core import Uri

WithSigner = bool
provider_uri = Uri.from_str("plugin/ethereum-provider")


def test_sign_message(client_factory: Callable[[WithSigner], PolywrapClient]):
    message = "Hello World".encode("utf-8")
    client = client_factory(True)
    result = client.invoke(
        uri=provider_uri,
        method="signMessage",
        args={"message": message},
        encode_result=False
    )

    assert result == "0xa4708243bf782c6769ed04d83e7192dbcf4fc131aa54fde9d889d8633ae39dab03d7babd2392982dff6bc20177f7d887e27e50848c851320ee89c6c63d18ca761c"
