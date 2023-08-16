"""This package contains the Polywrap Python SDK.

Installation
============
Install the package with pip:

.. code-block:: bash

    pip install polywrap

Quickstart
==========

Imports
-------

>>> from polywrap import (
...     Uri,
...     ClientConfig,
...     PolywrapClient,
...     PolywrapClientConfigBuilder,
...     sys_bundle,
...     web3_bundle
... )

Configure and Instantiate
-------------------------

>>> builder = (
...     PolywrapClientConfigBuilder()
...     .add_bundle(sys_bundle)
...     .add_bundle(web3_bundle)
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
from polywrap_client import *
from polywrap_client_config_builder import *
from polywrap_core import *
from polywrap_ethereum_provider import *
from polywrap_fs_plugin import *
from polywrap_http_plugin import *
from polywrap_manifest import *
from polywrap_msgpack import *
from polywrap_plugin import *
from polywrap_sys_config_bundle import *
from polywrap_uri_resolvers import *
from polywrap_wasm import *
from polywrap_web3_config_bundle import *
