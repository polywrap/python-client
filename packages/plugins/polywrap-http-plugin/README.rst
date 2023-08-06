Polywrap Http Plugin
====================
This package contains the HTTP plugin.

Http plugin currently supports two different methods `GET` and    `POST`. Similar to calling axios, when defining request    you need to specify a response type. Headers and     query parameters may also be defined.

Response Types
--------------

`TEXT` - The server will respond with text,     the HTTP plugin will return the text as-is.

`BINARY` - The server will respond with binary data (_bytes_),     the HTTP plugin will encode as a **base64** string and return it.

Quickstart
----------

Imports
~~~~~~~

>>> import json
>>> from polywrap_core import Uri
>>> from polywrap_client import PolywrapClient
>>> from polywrap_client_config_builder import PolywrapClientConfigBuilder
>>> from polywrap_http_plugin import http_plugin
>>> from polywrap_msgpack import GenericMap

Create a Polywrap client
~~~~~~~~~~~~~~~~~~~~~~~~

>>> http_interface_uri = Uri.from_str("wrap://ens/wraps.eth:http@1.0.0")
>>> http_plugin_uri = Uri.from_str("plugin/http")
>>> config = (
...     PolywrapClientConfigBuilder()
...     .set_package(http_plugin_uri, http_plugin())
...     .add_interface_implementations(http_interface_uri, [http_plugin_uri])
...     .set_redirect(http_interface_uri, http_plugin_uri)
...     .build()
... )
>>> client = PolywrapClient(config)

Make a GET request
~~~~~~~~~~~~~~~~~~

>>> result = client.invoke(
...     uri=http_interface_uri,
...     method="get",
...     args={
...         "url": "https://jsonplaceholder.typicode.com/posts",
...         "request": {
...             "responseType": "TEXT",
...             "urlParams": GenericMap({"id": 1}),
...             "headers": GenericMap({"X-Request-Header": "req-foo"}),
...         },
...     }
... )
>>> result.get("status")
200

Make a POST request
~~~~~~~~~~~~~~~~~~~

>>> result = client.invoke(
...     uri=http_interface_uri,
...     method="post",
...     args={
...         "url": "https://jsonplaceholder.typicode.com/posts",
...         "request": {
...             "responseType": "TEXT",
...             "body": json.dumps({
...                 "userId": 11,
...                 "id": 101,
...                 "title": "foo",
...                 "body": "bar"
...             }),
...             "headers": GenericMap({"X-Request-Header": "req-foo"}),
...         },
...     }
... )
>>> result.get("status")
201
