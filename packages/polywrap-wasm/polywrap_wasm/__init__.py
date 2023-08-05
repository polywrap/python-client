"""This package contains the runtime for executing Wasm wrappers.

Quickstart
----------
The following code snippet demonstrates how to use the runtime to execute a Wasm wrapper.

Imports
~~~~~~~

>>> import os
>>> from typing import cast
>>> from polywrap_core import Uri, FileReader, InvokerClient
>>> from polywrap_wasm import WasmWrapper
>>> from polywrap_msgpack import msgpack_decode
>>> from polywrap_manifest import deserialize_wrap_manifest, AnyWrapManifest

Create a Wasm wrapper
~~~~~~~~~~~~~~~~~~~~~

>>> path_to_wrapper = os.path.join(os.path.dirname(__file__), "..", "tests", "cases", "simple")
>>> assert os.path.exists(path_to_wrapper)
>>> with open(os.path.join(path_to_wrapper, "wrap.wasm"), "rb") as f:
...     wasm_module = f.read()
>>> assert isinstance(wasm_module, bytes)
>>> with open(os.path.join(path_to_wrapper, "wrap.info"), "rb") as f:
...     manifest = deserialize_wrap_manifest(f.read())
>>> assert isinstance(manifest, AnyWrapManifest)
>>> wrapper = WasmWrapper(
...     cast(FileReader, NotImplemented),
...     wasm_module,
...     manifest
... )
>>> assert isinstance(wrapper, WasmWrapper)

Invocation
~~~~~~~~~~

>>> message = "Hello, World!"
>>> args = {"arg": message}
>>> result = wrapper.invoke(
...     uri=Uri.from_str("wrap://authority/path"),
...     method="simpleMethod",
...     args=args,
...     client=cast(InvokerClient, NotImplemented),
... )
>>> assert result.encoded is True
>>> assert msgpack_decode(cast(bytes, result.result)) == message
"""
from .errors import *
from .inmemory_file_reader import *
from .wasm_package import *
from .wasm_wrapper import *
