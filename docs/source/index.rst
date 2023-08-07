.. polywrap-client documentation master file, created by
   sphinx-quickstart on Mon Mar 20 14:56:45 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to polywrap-client's documentation!
===========================================

Quickstart
==========

Imports
-------

>>> from polywrap_core import Uri, ClientConfig
>>> from polywrap_client import PolywrapClient
>>> from polywrap_client_config_builder import PolywrapClientConfigBuilder
>>> from polywrap_sys_config_bundle import get_sys_config

Configure and Instantiate
-------------------------

>>> builder = (
...     PolywrapClientConfigBuilder()
...     .add(get_sys_config())
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


.. toctree::
   :maxdepth: 1
   :caption: Contents:

   polywrap-client/modules.rst
   polywrap-client-config-builder/modules.rst
   polywrap-fs-plugin/modules.rst
   polywrap-http-plugin/modules.rst
   polywrap-ethereum-provider/modules.rst
   polywrap-sys-config-bundle/modules.rst
   polywrap-web3-config-bundle/modules.rst
   polywrap-msgpack/modules.rst
   polywrap-manifest/modules.rst
   polywrap-core/modules.rst
   polywrap-wasm/modules.rst
   polywrap-plugin/modules.rst
   polywrap-uri-resolvers/modules.rst

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
