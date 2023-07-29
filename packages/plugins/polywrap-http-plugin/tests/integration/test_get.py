from base64 import b64decode
import json
from mocket import mocketize
from polywrap_http_plugin import Response
from polywrap_core import Uri

from .mock_http import create_client

@mocketize
def test_simple_get():
    client = create_client()

    response: Response = client.invoke(
        uri=Uri.from_str("wrapper/integration"),
        method="get",
        args={
            "url": "https://example.none/todos/1",
            "request": {
                "responseType": 0,
            },
        },
    )

    assert response["status"] == 200
    assert response["body"] is not None
    assert json.loads(response["body"])["id"] == 1


@mocketize
def test_params_get():
    client = create_client()

    response: Response = client.invoke(
        uri=Uri.from_str("wrapper/integration"),
        method="get",
        args={
            "url": "https://example.none/todos",
            "request": {
                "responseType": 0,
                "urlParams": {
                    "id": "2",
                },
            },
        },
    )

    assert response["status"] == 200
    assert response["body"] is not None
    assert json.loads(response["body"])["id"] == 2

@mocketize
def test_binary_get():
    client = create_client()

    response: Response = client.invoke(
        uri=Uri.from_str("wrapper/integration"),
        method="get",
        args={
            "url": "https://example.none/todos/1",
            "request": {
                "responseType": 1,
            },
        },
    )

    assert response["status"] == 200
    assert response["body"] is not None
    assert json.loads(b64decode(response["body"]).decode("utf-8"))["id"] == 1
