"""This module implements the msgpack decoder for decoding data \
    recieved from a wrapper."""
from __future__ import annotations

from typing import Any

import msgpack

from .errors import MsgpackDecodeError, MsgpackExtError
from .extensions import ExtensionTypes, GenericMap


def decode_ext_hook(code: int, data: bytes) -> Any:
    """Extension hook for extending the msgpack supported types.

    Args:
        code (int): extension type code (>0 & <256)
        data (bytes): msgpack deserializable data as payload

    Raises:
        MsgpackExtError: when given invalid extension type code
        MsgpackDecodeError: when payload for extension type is invalid

    Returns:
        Any: decoded object
    """
    if code == ExtensionTypes.GENERIC_MAP.value:
        return GenericMap(msgpack_decode(data))
    raise MsgpackExtError("Invalid extention type")


def msgpack_decode(val: bytes) -> Any:
    """Decode msgpack bytes into a valid python object.

    Args:
        val (bytes): msgpack encoded bytes

    Raises:
        MsgpackExtError: when given invalid extension type code
        MsgpackDecodeError: when given invalid msgpack data

    Returns:
        Any: any python object
    """
    try:
        return msgpack.unpackb(
            val, ext_hook=decode_ext_hook
        )  # pyright: reportUnknownMemberType=false
    except Exception as e:
        raise MsgpackDecodeError("Failed to decode msgpack data") from e
