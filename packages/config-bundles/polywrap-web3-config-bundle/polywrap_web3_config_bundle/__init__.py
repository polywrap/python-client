"""This package contains the system configuration bundle for Polywrap Client.

Bundled Wraps
-------------

.. csv-table::
    :header: "wrap", "description"

    "http", "To make HTTP requests"
    "ipfs_http_client", "To add or retrieve items from IPFS"
    "ipfs_resolver", "To fetch wraps from IPFS"
    "ethereum_provider", "To perform ethereum RPC calls"
    "ethereum-wrapper", "A higher level API to perform ethereum operations (like etheres.js)"
    "ens_text_record_resolver", "To resolve URIs from ens text record"
    "ens_ipfs_contenthash_resolver", "To resolve URIs from ens content hash"
    "ens_resolver", "To resolve URIs from ens"

Quickstart
----------

Imports
~~~~~~~

>>> from polywrap_client_config_builder import PolywrapClientConfigBuilder
>>> from polywrap_web3_config_bundle import web3_bundle
>>> from polywrap_client import PolywrapClient
>>> from polywrap_core import Uri, UriPackage

Configure
~~~~~~~~~

>>> config = PolywrapClientConfigBuilder().add_bundle(web3_bundle).build()
>>> client = PolywrapClient(config)

Resolve URI with bundled ens resolver
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

>>> response = client.try_resolve_uri(
...     Uri.from_str("wrap://ens/wrap-link.eth")
... )
>>> assert isinstance(response, UriPackage)
"""
from .bundle import *
