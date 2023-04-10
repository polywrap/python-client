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

// add or remove items by chaining method calls
builder
    .add_package("wrap://plugin/package", test_plugin({}))
    .remove_package("wrap://plugin/package")
    .add_packages(
      {
        "wrap://plugin/http": http_plugin({}),
        "wrap://plugin/filesystem": file_system_plugin({}),
      }
    )
```

### Build

Finally, build a ClientConfig to pass to the PolywrapClient constructor.

```python
# accepted by the PolywrapClient
config = builder.build()

# build with a custom cache
config = builder.build({
  wrapperCache: WrapperCache(),
})

# or build with a custom resolver
coreClientConfig = builder.build({
  resolver: RecursiveResolver(...),
})
```
