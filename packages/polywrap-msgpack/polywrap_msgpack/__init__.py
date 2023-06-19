"""
polywrap-msgpack adds ability to encode/decode to/from msgpack format.

It provides msgpack_encode and msgpack_decode functions
which allows user to encode and decode to/from msgpack bytes

It also defines the default Extension types and extension hook for
custom extension types defined by WRAP standard
"""
from .decoder import *
from .encoder import *
from .errors import *
from .extensions import *
from .sanitize import *
