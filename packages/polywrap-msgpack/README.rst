Polywrap Msgpack
================

polywrap-msgpack adds ability to encode/decode to/from msgpack format.

It provides msgpack_encode and msgpack_decode functions
which allows user to encode and decode to/from msgpack bytes

It also defines the default Extension types and extension hook for
custom extension types defined by WRAP standard

Quickstart
----------

Encoding-Decoding Native types and objects
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

>>> from polywrap_msgpack import msgpack_decode, msgpack_encode
>>> dictionary = {
...     "foo": 5,
...     "bar": [True, False],
...     "baz": {
...         "prop": "value"
...     }
... }
>>> encoded = msgpack_encode(dictionary)
>>> decoded = msgpack_decode(encoded)
>>> assert dictionary == decoded
>>> print(decoded)
{'foo': 5, 'bar': [True, False], 'baz': {'prop': 'value'}}
    
Encoding-Decoding Extension types
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

>>> from polywrap_msgpack import msgpack_decode, msgpack_encode, GenericMap
>>> counter: GenericMap[str, int] = GenericMap({
...     "a": 3,
...     "b": 2,
...     "c": 5
... })
>>> encoded = msgpack_encode(counter)
>>> decoded = msgpack_decode(encoded)
>>> assert counter == decoded
>>> print(decoded)
GenericMap({'a': 3, 'b': 2, 'c': 5})
