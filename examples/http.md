# Http Wrap Example

In this document, we walk through a Python script that demonstrates how
to use the Polywrap client with HTTP plugin to send HTTP requests.

## Imports

To start, we import the required modules and functions:

<!-- name: test_http -->
```python
from polywrap import (
    Uri,
    PolywrapClient,
    PolywrapClientConfigBuilder,
    http_plugin
)
```

## Polywrap Client Configuration Setup

Before making HTTP requests, we set up the configuration for the
Polywrap client:

### Create a PolywrapClientConfigBuilder

<!-- name: test_http -->
```python
config_builder = PolywrapClientConfigBuilder()
```

### Add the http_plugin to the config_builder

<!-- name: test_http -->
```python
config_builder.set_package(Uri.from_str("wrapscan.io/polywrap/http@1.0"), http_plugin())
```

### Build the PolywrapClientConfig

<!-- name: test_http -->
```python
config = config_builder.build()
```

## Initialize the Polywrap Client

With our configuration ready, we instantiate the Polywrap client:

<!-- name: test_http -->
```python
client = PolywrapClient(config)
```

## HTTP GET Request

Using the Polywrap client, we send a GET request:

<!-- 
    name: test_http;
    case: get;
-->
```python
get_response = client.invoke(
    uri=Uri.from_str("wrapscan.io/polywrap/http@1.0"),
    method="get",
    args={
        "url": "https://jsonplaceholder.typicode.com/posts/1",
    },
)
print(get_response)
assert get_response["status"] == 200
```

## HTTP POST Request

Similarly, we send a POST request:

<!-- 
    name: test_http;
    case: post;
-->
```python
post_response = client.invoke(
    uri=Uri.from_str("wrapscan.io/polywrap/http@1.0"),
    method="post",
    args={
        "url": "https://jsonplaceholder.typicode.com/posts",
        "body": {
            "id": 101,
            "userId": 101,
            "title": "Test Title",
            "body": "Test Body",
        },
    },
)
print(post_response)
assert post_response["status"] == 201
```

## Conclusion

This document provides a brief walkthrough of how to use the Polywrap
client with the HTTP plugin to make GET and POST requests.
For more information on the `PolywrapClient`, please refer to the 
[Polywrap Python Client documentation](https://polywrap-client.rtfd.io).
