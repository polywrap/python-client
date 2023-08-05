"""This package contains the implementation of polywrap python client.

Quickstart
==========

Configure and Instantiate
-------------------------

Use the `polywrap-uri-resolvers` package to configure resolver and build config for the client.

>>> from polywrap_uri_resolvers import (
...     FsUriResolver,
...     SimpleFileReader
... )
>>> from polywrap_core import Uri, ClientConfig
>>> from polywrap_client import PolywrapClient
>>> from polywrap_client_config_builder import PolywrapClientConfigBuilder
>>> from polywrap_sys_config_bundle import get_sys_config
>>> builder = (
...     PolywrapClientConfigBuilder()
...     .add(get_sys_config())
...     .set_env(Uri.from_str("ens/foo.eth"), {"foo": "bar"})
...     .add_interface_implementations(
...         Uri.from_str("ens/foo.eth"), [
...             Uri.from_str("ens/bar.eth"),
...             Uri.from_str("ens/baz.eth")
...         ]
...     )
... )
>>> config = builder.build()
>>> client = PolywrapClient(config)

Invocation
----------

Invoke a wrapper.

>>> uri = Uri.from_str(
...     'wrapscan.io/polywrap/ipfs-http-client'
... )
>>> args = {
...     "cid": "QmZ4d7KWCtH3xfWFwcdRXEkjZJdYNwonrCwUckGF1gRAH9",
...     "ipfsProvider": "https://ipfs.io",
... }
>>> result = client.invoke(uri=uri, method="cat", args=args, encode_result=False)
>>> assert result.startswith(b"<svg")
"""
from .client import *
