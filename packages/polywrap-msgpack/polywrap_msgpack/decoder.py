"""This module implements the msgpack decoder for decoding data \
    recieved from a wrapper."""
from __future__ import annotations

from typing import Any

import msgpack
from msgpack.exceptions import UnpackValueError

from .extensions import ExtensionTypes, GenericMap


def decode_ext_hook(code: int, data: bytes) -> Any:
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
        return GenericMap(msgpack_decode(data))
    raise UnpackValueError("Invalid extention type")


def msgpack_decode(val: bytes) -> Any:
    """Decode msgpack bytes into a valid python object.

    Args:
        val (bytes): msgpack encoded bytes

    Raises:
        UnpackValueError: when given invalid extension type code

    Returns:
        Any: any python object
    """
    return msgpack.unpackb(
        val, ext_hook=decode_ext_hook
    )  # pyright: reportUnknownMemberType=false
