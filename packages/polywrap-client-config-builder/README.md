# polywrap-client-config-builder

A utility class for building the PolywrapClient config. 

Supports building configs using method chaining or imperatively.

## Quickstart

### Initialize

Initialize a ClientConfigBuilder using the constructor

```python
# start with a blank slate (typical usage)
builder = ClientConfigBuilder()
```

### Configure

Add client configuration with add, or flexibly mix and match builder configuration methods to add and remove configuration items.

```python
# add multiple items to the configuration using the catch-all `add` method
builder.add(
    BuilderConfig(
        envs={},
        interfaces={},
        redirects={},
        wrappers={},
        packages={},
        resolvers=[]
    )
)

# add or remove items by chaining method calls
builder
    .add_package("wrap://plugin/package", test_plugin({}))
    .remove_package("wrap://plugin/package")
    .add_packages(
      {
        "wrap://plugin/http": http_plugin({}),
        "wrap://plugin/filesystem": file_system_plugin({}),
      }
    )

# configure using sys config bundle to fetch wraps from file-system, ipfs, wrapscan, or http server
from polywrap_sys_config_bundle import get_sys_config
builder.add(get_sys_config())

# configure using web3 config bundle to fetch wraps from ens and any system URI
from polywrap_web3_config_bundle import get_web3_config
builder.add(get_web_config)
```

### Build

Finally, build a ClientConfig to pass to the PolywrapClient constructor.

```python
# accepted by the PolywrapClient
config = builder.build()

# build with a custom cache
config = builder.build({
  resolution_result_cache: ResolutionResultCache(),
})

# or build with a custom resolver
config = builder.build({
  resolver: RecursiveResolver(...),
})
```
