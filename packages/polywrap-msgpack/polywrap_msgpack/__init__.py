"""
polywrap-msgpack adds ability to encode/decode to/from msgpack format.

It provides msgpack_encode and msgpack_decode functions
which allows user to encode and decode to/from msgpack bytes

It also defines the default Extension types and extension hook for
custom extension types defined by wrap standard
"""
from enum import Enum
from typing import Any, Dict, List, Set

import msgpack
from msgpack.exceptions import UnpackValueError


class ExtensionTypes(Enum):
    """Wrap msgpack extension types."""

    GENERIC_MAP = 1


def ext_hook(code: int, data: bytes) -> Any:
    """Extension hook for extending the msgpack supported types.

    Args:
        code (int): extension type code (>0 & <256)
        data (bytes): msgpack deserializable data as payload

    Raises:
        UnpackValueError: when given invalid extension type code

    Returns:
        Any: decoded object
    """
    if code == ExtensionTypes.GENERIC_MAP.value:
        return msgpack_decode(data)
    raise UnpackValueError("Invalid Extention type")


def sanitize(value: Any) -> Any:
    """Sanitizes the value into msgpack encoder compatible format.

    Args:
        value: any valid python value

    Raises:
        ValueError: when dict key isn't string

    Returns:
        Any: msgpack compatible sanitized value
    """
    if value.__class__.__name__ == "Uri":
        raise TypeError("Uri is not supported by msgpack")

    if isinstance(value, dict):
        dictionary: Dict[Any, Any] = value
        for key, val in list(dictionary.items()):
            # try:
            #     print(f"{key=}")
            #     print(f"{key.uri=}")
            # except:
            #     pass
            if isinstance(key, str):
                print(f"{key=}")
                print(f"{type(key)=}")
                print(f"{val=}")
                print(f"{type(val)=}")
                dictionary[key] = sanitize(val)
            elif key.uri:
                print(f"Found Key and it has uri")
                print(f"{type(key)=}")
                print(f"{key.uri=}")
                print(f"{type(key.uri)=}")
                print(f"{val=}")
                print(f"{type(val)=}")
                dictionary[key] = sanitize(val)
            else:                
                raise ValueError(
                    f"expected dict key to be str received {key} with type {type(key)}"
                )
        return dictionary
    if isinstance(value, list):
        array: List[Any] = value
        return [sanitize(a) for a in array]
    if isinstance(value, tuple):
        array: List[Any] = list(value)  # type: ignore
        return sanitize(array)
    if isinstance(value, set):
        set_val: Set[Any] = value
        return list(set_val)
    if isinstance(value, complex):
        return str(value)
    if hasattr(value, "__slots__"):
        # answer: Dict[str,Any] = {}
        # for s in getattr(value, "__slots__"):
        #     print(f"{s=}")
        #     if hasattr(value, s):
        #         answer.update({s: sanitize(getattr(value, s))})
        #     if hasattr(value.uri, 'authority'):
        #         # print(value[s])
        #         answer.update({s: sanitize(getattr(value.uri, 'uri'))})
        #         print(f"!- Found {value.uri=}")
        #         print(f"!- Found {value.uri.authority=}")
            
        # return answer

        return {
            s: sanitize(getattr(value, s))
            for s in getattr(value, "__slots__")
            if hasattr(value, s)
        }
    if hasattr(value, "__dict__"):
        answer: Dict[str, Any] = {}
        for k, v in vars(value).items():
            print(f"{k=}")
            print(f"{v=}")
            if not isinstance(k, str):
                answer.update({k.uri:sanitize(v)})
            if isinstance(k, str):
                answer.update({k:sanitize(v)})
            # elif k.uri:
            #     answer.update({k.uri:sanitize(v)})
            
        return answer
        return {k: sanitize(v) for k, v in vars(value).items()}
    return value


def msgpack_encode(value: Any) -> bytes:
    """Encode any python object into msgpack bytes.

    Args:
        value: any valid python object

    Returns:
        bytes: encoded msgpack value
    """
    print(f"{value=}")
    if value.__class__.__name__ == "Uri":
        raise ValueError("Uri is not supported by msgpack")
    sanitized = sanitize(value)

    return msgpack.packb(sanitized)


def msgpack_decode(val: bytes) -> Any:
    """Decode msgpack bytes into a valid python object.

    Args:
        val: msgpack encoded bytes

    Returns:
        Any: python object
    """
    if val.__class__.__name__ == 'Uri':
           raise TypeError("Cannot encode Uri")
    return msgpack.unpackb(val, ext_hook=ext_hook)
