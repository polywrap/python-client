import json

from polywrap_http_plugin import http_plugin
from polywrap_client import PolywrapClient
from polywrap_core import Uri
from polywrap_client_config_builder import PolywrapClientConfigBuilder

from mocket.mockhttp import Entry


def mock_get_response(url_to_mock: str, id: int):
    Entry.single_register(
        Entry.GET,
        url_to_mock,
        body=json.dumps({"id": id}),
        headers={"content-type": "application/json"},
    )

def mock_post_response(url_to_mock: str, id: int):
    Entry.single_register(
        Entry.POST,
        url_to_mock,
        body=json.dumps({"id": id}),
        headers={"content-type": "application/json"},
        status=201,
    )


def create_client():
    mock_get_response("https://example.none/todos/1", 1)
    mock_get_response("https://example.none/todos?id=2", 2)
    mock_get_response("https://example.none/todos/3?userId=1", 4)
    mock_post_response("https://example.none/todos", 101)

    builder = PolywrapClientConfigBuilder().set_package(
        Uri.from_str("plugin/http"), http_plugin()
    )
    config = builder.build()
    return PolywrapClient(config)
