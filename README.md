![Public Release Announcement](https://user-images.githubusercontent.com/5522128/177473887-2689cf25-7937-4620-8ca5-17620729a65d.png)

# Polywrap Python Client

[Polywrap](https://polywrap.io) is a protocol for building and executing composable wrappers for any web3 protocol. Polywrap Python Client is a Python library that allows you to easily execute Polywrap Wrappers.

## Quickstart

### Install the package

```bash
pip install polywrap
```

### Import necessary packages

```python
from polywrap import (
    Uri,
    ClientConfig,
    PolywrapClient,
    PolywrapClientConfigBuilder,
    sys_bundle,
    web3_bundle
)
```

### Configure and Instantiate the client
```python
builder = (
    PolywrapClientConfigBuilder()
    .add_bundle(sys_bundle)
    .add_bundle(web3_bundle)
)
config = builder.build()
client = PolywrapClient(config)
```

### Invoke a wrapper

```python
uri = Uri.from_str(
    'wrapscan.io/polywrap/ipfs-http-client'
)
args = {
    "cid": "QmZ4d7KWCtH3xfWFwcdRXEkjZJdYNwonrCwUckGF1gRAH9",
    "ipfsProvider": "https://ipfs.io",
}
result = client.invoke(uri=uri, method="cat", args=args, encode_result=False)
assert result.startswith(b"<svg")
```

## Working Features

[Here](https://github.com/polywrap/client-test-harness) you can see which features have been implemented on each language client, and make the decision of which one to use for your project.

## Feedback & Contributions
Bugs and feature requests can be made via [GitHub issues](https://github.com/polywrap/python-client/issues). Be aware that these issues are not private, so take care when providing output to make sure you are not disclosing any personal informations.

[Pull requests](https://github.com/polywrap/python-client/pulls) are also welcome via git.

New contributors should read the [contributor guide](./CONTRIBUTING.rst) to get started.
Folk who already have experience contributing to open source projects may not need the full guide but should still use the pull request checklist to make things easy for everyone.
Polywrap Python Client contributors are asked to adhere to the [Python Community Code of Conduct](https://www.python.org/psf/conduct/).

# Contact Us:

[Join our discord](https://discord.polywrap.io) and ask your questions right away!

# Resources

- [Polywrap Documentation](https://docs.polywrap.io)
- [Python Client Documentation](https://polywrap-client.rtfd.io)
- [Client Readiness](https://github.com/polywrap/client-readiness)
- [Discover Wrappers](https://wrapscan.io)
- [Polywrap Discord](https://discord.polywrap.io)
