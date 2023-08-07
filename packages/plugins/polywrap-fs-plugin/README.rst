Polywrap Fs Plugin
==================
The Filesystem plugin enables wraps running within the Polywrap client    to interact with the local filesystem.

Interface
---------

The FileSystem plugin implements an existing wrap interface at     `wrap://ens/wraps.eth:file-system@1.0.0`.

Quickstart
----------

Imports
~~~~~~~

>>> import os
>>> from polywrap_core import Uri
>>> from polywrap_client import PolywrapClient
>>> from polywrap_client_config_builder import PolywrapClientConfigBuilder
>>> from polywrap_fs_plugin import file_system_plugin

Create a Polywrap client
~~~~~~~~~~~~~~~~~~~~~~~~

>>> fs_interface_uri = Uri.from_str("wrap://ens/wraps.eth:file-system@1.0.0")
>>> fs_plugin_uri = Uri.from_str("plugin/file-system")
>>> config = (
...     PolywrapClientConfigBuilder()
...     .set_package(fs_plugin_uri, file_system_plugin())
...     .add_interface_implementations(fs_interface_uri, [fs_plugin_uri])
...     .set_redirect(fs_interface_uri, fs_plugin_uri)
...     .build()
... )
>>> client = PolywrapClient(config)

Invoke the plugin
~~~~~~~~~~~~~~~~~

>>> path = os.path.join(os.path.dirname(__file__), "..", "pyproject.toml")
>>> result = client.invoke(
...     uri=Uri.from_str("wrap://ens/wraps.eth:file-system@1.0.0"),
...     method="readFile",
...     args={
...         "path": path,
...     }
... )
>>> assert result.startswith(b"[build-system]")
