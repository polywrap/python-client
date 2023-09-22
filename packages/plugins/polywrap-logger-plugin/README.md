# Logger Python Plugin
The Logger plugin implements the `logger-interface` from the `ens/wraps.eth:logger@1.0.0` package (see [./src/schema.graphql](./src/schema.graphql)). By default, it logs all events using the Python `logging` module. You can customize this behavior by setting the `Logger` property on the plugin's configuration object (examples below).

## Usage
### 1. Configure Client
When creating your Polywrap Python client, add the logger plugin:
```python
from polywrap_client_config_builder  import PolywrapClientConfigBuilder
from polywrap_logger_plugin import logger_plugin
from polywrap_client import PolywrapClient

config = PolywrapClientConfigBuilder().set_package(
    uri=Uri.from_str("plugin/logger"),
    package=logger_plugin()
).set_interface(
    interface=Uri.from_str("ens/wraps.eth:logger@1.0.0"),
    implementations=[Uri.from_str("plugin/logger")]
).set_redirect(
    Uri.from_str("ens/wraps.eth:logger@1.0.0"),
    Uri.from_str("plugin/logger")
).build()
client = PolywrapClient(config)
```

### 2. Invoke The Logger
Invocations to the logger plugin can be made via the interface URI (which will get redirected), or the plugin's URI directly:
```python
await client.invoke({
  'uri': 'ens/wraps.eth:logger@1.0.0' | 'plugin/logger',
  'method': 'log',
  'args': {
    'level': 'INFO',
    'message': 'foo bar baz'
  }
})
```

### 3. Customize The Logger
When adding the logger to your client, you can add your own custom log function:
```python
config = PolywrapClientConfigBuilder().set_package(
    uri=Uri.from_str("plugin/logger"),
    package=logger_plugin(LoggerConfig(logger=YourLogger(), level=LogLevel.INFO))
).set_interface(
    interface=Uri.from_str("ens/wraps.eth:logger@1.0.0"),
    implementations=[Uri.from_str("plugin/logger")]
).set_redirect(
    Uri.from_str("ens/wraps.eth:logger@1.0.0"),
    Uri.from_str("plugin/logger")
).build()
```

### 4. Add Multiple Loggers
Multiple logger implementations can be added to the client:
```python
config = PolywrapClientConfigBuilder().set_package(
    uri=Uri.from_str("plugin/logger"),
    package=logger_plugin(LoggerConfig(logger=YourLogger(), level=LogLevel.INFO))
).set_interface(
    interface=Uri.from_str("ens/wraps.eth:logger@1.0.0"),
    implementations=[Uri.from_str("plugin/logger"), Uri.from_str("plugin/custom-logger")]
).set_package(
    uri=Uri.from_str("plugin/custom-logger"),
    package=custom_logger_plugin()
).build()
```

### 5. Invoke All Logger Implementations
When you'd like to log something to more than one logger, you can invoke all implementations of the logger interface:
```python
implementations = client.get_implementations('ens/wraps.eth:logger@1.0.0')

for impl in implementations:
    await client.invoke({
        'uri': impl,
        'method': 'log',
        'args': {
            'level': 'INFO',
            'message': 'message'
        }
    })
```