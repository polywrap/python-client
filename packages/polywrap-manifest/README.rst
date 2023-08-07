Polywrap Manifest
=================
Polywrap Manifest contains the types and functions to de/serialize  Wrap manifests defined at https://github.com/polywrap/wrap.

Quickstart
----------

Deserialize WRAP manifest
~~~~~~~~~~~~~~~~~~~~~~~~~

>>> from polywrap_manifest import deserialize_wrap_manifest, WrapManifest_0_1
>>> from polywrap_msgpack import msgpack_encode
>>> raw_manifest = msgpack_encode({
...     "version": "0.1.0",
...     "type": "interface",
...     "name": "test-interface",
...     "abi": {},
... })
>>> manifest = deserialize_wrap_manifest(raw_manifest)
>>> assert isinstance(manifest, WrapManifest_0_1)
