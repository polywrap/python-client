# IPFS Wrap Example

In this guide, we\'ll walk through a Python script that demonstrates how
to use the Polywrap client to upload and download data from IPFS.

## Pre-Requisites

Before executing this script, ensure you have an IPFS node running
locally. This can be accomplished using the command:

```
npx polywrap infra up --modules=eth-ens-ipfs
```

## Imports

First, we import the necessary modules and functions:

<!-- name: test_ipfs -->
```python
from polywrap import Uri, PolywrapClient, PolywrapClientConfigBuilder, sys_bundle
```

## Polywrap Configuration

To interact with IPFS via Polywrap, we need to set up the client\'s
configuration:

### Create a PolywrapClientConfigBuilder

<!-- name: test_ipfs -->
```python
config_builder = PolywrapClientConfigBuilder()
```

### Include the system config bundle

<!-- name: test_ipfs -->
```python
config_builder.add_bundle(sys_bundle)
```

### Build the PolywrapClientConfig

<!-- name: test_ipfs -->
```python
config = config_builder.build()
```

### Initialize the Polywrap Client

<!-- name: test_ipfs -->
```python
client = PolywrapClient(config)
```

## Initialization

Set up the necessary variables for interacting with IPFS:

<!-- name: test_ipfs -->
```python
uri = Uri.from_str("wrapscan.io/polywrap/ipfs-http-client@1.0")
ipfs_provider = "http://localhost:5001"
file_name = "test.txt"
file_data = b"Hello World!"

print(f"File Name: {file_name}")
print(f"File Data: {file_data}")
```

## Uploading to IPFS

With our setup complete, we can proceed to upload a file to IPFS:

<!-- 
    name: test_ipfs;
    case: upload;
-->
```python
add_file_response = client.invoke(
    uri=uri,
    method="addFile",
    args={
        "data": {
            "name": file_name,
            "data": file_data
        },
        "ipfsProvider": ipfs_provider
    }
)
ipfs_hash = add_file_response["hash"]
print(f"IPFS Hash: {ipfs_hash}")
assert ipfs_hash is not None
```

## Downloading from IPFS

Finally, we\'ll download the previously uploaded file using its IPFS
hash:

<!-- 
    name: test_ipfs;
    case: download;
-->
```python
downloaded_file_data = client.invoke(
    uri=uri,
    method="cat",
    args={
        "cid": ipfs_hash,
        "ipfsProvider": ipfs_provider
    }
)

print(f"Downloaded File Data: {downloaded_file_data}")
assert downloaded_file_data == file_data
```

## Conclusion

This guide showcases a basic interaction with IPFS using the Polywrap
client. This method provides a convenient way to work with IPFS without
directly interacting with the IPFS protocol.
