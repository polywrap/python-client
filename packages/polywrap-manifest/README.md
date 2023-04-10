# polywrap-manifest

Python implementation of the WRAP manifest schema at https://github.com/polywrap/wrap

## Usage

### Deserialize WRAP manifest

```python
from polywrap_manifest import deserialize_wrap_manifest, WrapManifest_0_1

with open("<path to WRAP package>/wrap.info", "rb") as f:
    raw_manifest = f.read()

manifest = deserialize_wrap_manifest(raw_manifest)
assert isinstance(manifest, WrapManifest_0_1)
```
