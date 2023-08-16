# Filesystem Wrap Example

In this document, we will walk through a Python script that uses the
Polywrap client to interact with a filesystem. We'll go step by step
explaining each section.

## Initial Setup

First, we import the necessary libraries:

<!-- name: test_filesystem -->
```python
from polywrap import Uri, PolywrapClient, PolywrapClientConfigBuilder, file_system_plugin
```

Now, let's create a URI for the specific plugin we want to access:

<!-- name: test_filesystem -->
```python
uri_string = Uri.from_str("wrapscan.io/polywrap/file-system@1.0")
```

## Building Configuration

We initialize a configuration builder and the filesystem plugin, then
set the package:

<!-- name: test_filesystem -->
```python
config_builder = PolywrapClientConfigBuilder()
fs_plugin = file_system_plugin()
config_builder.set_package(uri_string, fs_plugin)
```

## Initialize Polywrap Client

With our configuration ready, we create a Polywrap client instance:

<!-- name: test_filesystem -->
```python
client = PolywrapClient(config_builder.build())
```

## Setup File Parameters

Here we define the file path and the data we want to write:

<!-- name: test_filesystem -->
```python
file_path = "./fs-example.txt"
data = "Hello world!"
```

## Write to File

Next, we attempt to write data to the file:

<!-- name: test_filesystem -->
```python
try:
    write_file_result = client.invoke(
        uri=uri_string,
        method="writeFile",
        args={
            "path": file_path,
            "data": data.encode('utf-8')
        }
    )
    print("File created!")
except Exception as e:
    raise IOError("Error writing file") from e
```

## Read from File

Now we attempt to read data from the file:

<!-- name: test_filesystem -->
```python
try:
    read_file_result = client.invoke(
        uri=uri_string,
        method="readFile",
        args={
            "path": file_path
        }
    )
    print(f"Content file: {read_file_result.decode('utf-8')}")
except Exception as e:
    raise IOError("Error reading file") from e
```

## Remove File

Lastly, we try to remove the file:

<!-- name: test_filesystem -->
```python
try:
    remove_file_result = client.invoke(
        uri=uri_string,
        method="rm",
        args={
            "path": file_path
        }
    )
    print("File removed!")
except Exception as e:
    raise IOError("Error removing file") from e
```

## Conclusion

This example demonstrates how to use the `PolywrapClient` to interact with the Filesystem.
For more information on the `PolywrapClient`, please refer to the 
[Polywrap Python Client documentation](https://polywrap-client.rtfd.io).
