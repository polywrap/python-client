# polywrap-msgpack

Python implementation of the WRAP MsgPack encoding standard.

## Usage

### Encoding-Decoding Native types and objects

```python
from polywrap_msgpack import msgpack_decode, msgpack_encode

dictionary = {
  "foo": 5,
  "bar": [True, False],
  "baz": {
    "prop": "value"
  }
}

encoded = msgpack_encode(dictionary)
decoded = msgpack_decode(encoded)

assert dictionary == decoded
```

### Encoding-Decoding Extension types

```python
from polywrap_msgpack import msgpack_decode, msgpack_encode, GenericMap

counter: GenericMap[str, int] = GenericMap({
  "a": 3,
  "b": 2,
  "c": 5
})

encoded = msgpack_encode(counter)
decoded = msgpack_decode(encoded)

assert counter == decoded
```