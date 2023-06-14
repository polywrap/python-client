from typing import Any
from polywrap_core import (
    Client,
    Uri,
    get_env_from_resolution_path,
)
import pytest


@pytest.fixture
def resolution_path() -> list[Any]:
    return [
        Uri.from_str("test/1"),
        Uri.from_str("test/2"),
        Uri.from_str("test/3"),
    ]


@pytest.fixture
def client() -> Any:
    class MockClient:
        def get_env_by_uri(self, uri: Uri) -> Any:
            if uri.uri == "wrap://test/3":
                return {
                    "arg1": "arg1",
                    "arg2": "arg2",
                }

    return MockClient()


def test_get_env_from_resolution_path(resolution_path: list[Any], client: Client):
    assert get_env_from_resolution_path(resolution_path, client) == {
        "arg1": "arg1",
        "arg2": "arg2",
    }


def test_get_env_from_resolution_path_empty(client: Client):
    assert get_env_from_resolution_path([], client) is None
