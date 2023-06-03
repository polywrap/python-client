from polywrap_core import (
    Any,
    Client,
    Uri,
    get_implementations,
)
import pytest

interface_1 = Uri.from_str("wrap://ens/interface-1.eth")
interface_2 = Uri.from_str("wrap://ens/interface-2.eth")
interface_3 = Uri.from_str("wrap://ens/interface-3.eth")

implementation_1 = Uri.from_str("wrap://ens/implementation-1.eth")
implementation_2 = Uri.from_str("wrap://ens/implementation-2.eth")
implementation_3 = Uri.from_str("wrap://ens/implementation-3.eth")


redirects = {
    interface_1: interface_2,
    implementation_1: implementation_2,
    implementation_2: implementation_3,
}

interfaces = {
    interface_1: [implementation_1, implementation_2],
    interface_2: [implementation_3],
    interface_3: [implementation_3],
}


@pytest.fixture
def client() -> Any:
    class MockClient:
        def try_resolve_uri(self, uri: Uri, *args: Any) -> Uri:
            return redirects.get(uri, uri)

    return MockClient()


def test_get_implementations_1(client: Client):
    result = get_implementations(interface_1, interfaces, client)

    assert result
    assert set(result) == {
        implementation_1,
        implementation_2,
        implementation_3,
    }


def test_get_implementations_2(client: Client):
    result = get_implementations(interface_2, interfaces, client)

    assert result
    assert set(result) == {
        implementation_1,
        implementation_2,
        implementation_3,
    }


def test_get_implementations_3(client: Client):
    result = get_implementations(interface_3, interfaces, client)

    assert result
    assert set(result) == {
        implementation_3,
    }


def test_implementations_not_redirected(client: Client):
    result = get_implementations(interface_1, {
        interface_1: [implementation_1],
    }, client)

    assert result
    assert set(result) == {
        implementation_1,
    }