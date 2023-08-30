Polywrap
========
This package contains the Polywrap Python SDK.

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
