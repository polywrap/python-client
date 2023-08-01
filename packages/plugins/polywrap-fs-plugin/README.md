# polywrap-fs-plugin

The Filesystem plugin enables wraps running within the Polywrap client to interact with the local filesystem.

## Interface

The FileSystem plugin implements an existing wrap interface at `wrap://ens/wraps.eth:file-system@1.0.0`.

## Usage

``` python
from polywrap_client import PolywrapClient
from polywrap_client_config_builder import PolywrapClientConfigBuilder
from polywrap_fs_plugin import file_system_plugin

fs_interface_uri = Uri.from_str("wrap://ens/wraps.eth:file-system@1.0.0")
fs_plugin_uri = Uri.from_str("plugin/file-system")

config = (
    PolywrapClientConfigBuilder()
    .set_package(fs_plugin_uri, file_system_plugin())
    .add_interface_implementations(fs_interface_uri, [fs_plugin_uri])
    .set_redirect(fs_interface_uri, fs_plugin_uri)
    .build()
)

client.invoke(
    uri=Uri.from_str("wrap://ens/wraps.eth:file-system@1.0.0"),
    method="readFile",
    args={
        "path": "./file.txt"
    }
);
```

For more usage examples see `src/__tests__`.
