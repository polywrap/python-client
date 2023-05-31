import pytest
from polywrap_core import Uri
from polywrap_client import PolywrapClient
from polywrap_client_config_builder import PolywrapClientConfigBuilder



def test_get_all_implementations_of_interface():
    interface1_uri = Uri.from_str("wrap://ens/some-interface1.eth")
    interface2_uri = Uri.from_str("wrap://ens/some-interface2.eth")
    interface3_uri = Uri.from_str("wrap://ens/some-interface3.eth")

    implementation1_uri = Uri.from_str("wrap://ens/some-implementation.eth")
    implementation2_uri = Uri.from_str("wrap://ens/some-implementation2.eth")
    implementation3_uri = Uri.from_str("wrap://ens/some-implementation3.eth")
    implementation4_uri = Uri.from_str("wrap://ens/some-implementation4.eth")

    builder = (
        PolywrapClientConfigBuilder()
        .set_redirect(interface1_uri, interface2_uri)
        .set_redirect(implementation1_uri, implementation2_uri)
        .set_redirect(implementation2_uri, implementation3_uri)
        .set_package(implementation4_uri, NotImplemented)
        .add_interface_implementations(interface1_uri, [implementation1_uri, implementation2_uri])
        .add_interface_implementations(interface2_uri, [implementation3_uri])
        .add_interface_implementations(interface3_uri, [implementation3_uri, implementation4_uri])
    )


    client = PolywrapClient(builder.build())

    implementations1 = client.get_implementations(interface1_uri)
    implementations2 = client.get_implementations(interface2_uri)
    implementations3 = client.get_implementations(interface3_uri)

    assert implementations1 is not None
    assert implementations2 is not None
    assert implementations3 is not None

    assert set(implementations1) == {implementation1_uri, implementation2_uri, implementation3_uri}
    assert set(implementations2) == {implementation1_uri, implementation2_uri, implementation3_uri}
    assert set(implementations3) == {implementation3_uri, implementation4_uri}
