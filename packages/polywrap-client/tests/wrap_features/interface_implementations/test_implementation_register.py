import pytest
from polywrap_core import Uri
from polywrap_client import PolywrapClient
from polywrap_client_config_builder import PolywrapClientConfigBuilder


def test_register_interface_implementations():
    interface_uri = Uri.from_str("wrap://ens/some-interface1.eth")
    implementation1_uri = Uri.from_str("wrap://ens/some-implementation1.eth")
    implementation2_uri = Uri.from_str("wrap://ens/some-implementation2.eth")

    builder = (
        PolywrapClientConfigBuilder()
        .add_interface_implementations(
            interface_uri, [implementation1_uri, implementation2_uri]
        )
        .set_redirect(Uri.from_str("uri/foo"), Uri.from_str("uri/bar"))
    )

    client = PolywrapClient(builder.build())

    interfaces = client.get_interfaces()

    assert interfaces == {interface_uri: [implementation1_uri, implementation2_uri]}

    implementations = client.get_implementations(
        interface_uri
    )

    assert implementations is not None
    assert set(implementations) == {implementation1_uri, implementation2_uri}
