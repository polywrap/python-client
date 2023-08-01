from base64 import b64decode
import json
from mocket import mocketize
from polywrap_http_plugin import Response
from polywrap_client import PolywrapClient
from polywrap_core import Uri

from .mock_http import create_client


@mocketize
def test_simple_post():
    client = create_client()
    response: Response = client.invoke(
        uri=Uri.from_str("plugin/http"),
        method="post",
        args={
            "url": "https://example.none/todos",
            "request": {
                "body": json.dumps(
                    {
                        "title": "foo",
                        "body": "bar",
                        "userId": 1,
                    }
                ),
            },
        },
    )

    assert response["status"] == 201
    assert response["body"] is not None
    assert json.loads(response["body"])["id"] == 101


@mocketize
def test_binary_post():
    client = create_client()
    response: Response = client.invoke(
        uri=Uri.from_str("plugin/http"),
        method="post",
        args={
            "url": "https://example.none/todos",
            "request": {
                "responseType": 1,
                "body": json.dumps(
                    {
                        "title": "foo",
                        "body": "bar",
                        "userId": 1,
                    }
                ),
            },
        },
    )

    assert response["status"] == 201
    assert response["body"] is not None
    assert json.loads(b64decode(response["body"]).decode("utf-8"))["id"] == 101
