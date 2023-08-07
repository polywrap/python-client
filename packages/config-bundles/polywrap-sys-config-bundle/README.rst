Polywrap Sys Config Bundle
==========================
This package contains the system configuration bundle for Polywrap Client.

Bundled Wraps
-------------

.. csv-table::
    :header: "wrap", "description"

    "http", "To make HTTP requests"
    "http_resolver", "To resolve URIs from HTTP server"
    "wrapscan_resolver", "To resolve URIs from wrapscan.io"
    "ipfs_http_client", "To add or retrieve items from IPFS"
    "ipfs_resolver", "To fetch wraps from IPFS"
    "github_resolver", "To fetch wraps from github repo"
    "file_system", "To perform file system operations"
    "file_system_resolver", "To fetch wraps from File System"

Quickstart
----------

Imports
~~~~~~~

>>> from polywrap_client_config_builder import PolywrapClientConfigBuilder
>>> from polywrap_sys_config_bundle import sys_bundle
>>> from polywrap_client import PolywrapClient
>>> from polywrap_core import Uri, UriPackage

Configure
~~~~~~~~~

>>> config = PolywrapClientConfigBuilder().add_bundle(sys_bundle).build()
>>> client = PolywrapClient(config)

Invoke bundled http plugin
~~~~~~~~~~~~~~~~~~~~~~~~~~

>>> response = client.invoke(
...     uri=Uri.from_str("ens/wraps.eth:http@1.1.0"),
...     method="get",
...     args={"url": "https://www.google.com"},
... )
>>> response.get("status")
200

Resolve URI with bundled wrapscan resolver
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

>>> response = client.try_resolve_uri(
...     Uri("wrapscan.io", "polywrap/uri-resolver@1.0"),
... )
>>> assert isinstance(response, UriPackage)
