"""This module implements the msgpack decoder for decoding data \
    recieved from a wrapper."""
from __future__ import annotations

from typing import Any

import msgpack

from .errors import MsgpackDecodeError, MsgpackExtError
from .extensions import ExtensionTypes, GenericMap


def _decode_ext_hook(code: int, data: bytes) -> Any:
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
    r"""Decode msgpack bytes into a valid python object.

    Args:
        val (bytes): msgpack encoded bytes

    Raises:
        MsgpackExtError: when given invalid extension type code
        MsgpackDecodeError: when given invalid msgpack data

    Returns:
        Any: any python object

    Examples:
        >>> from polywrap_msgpack import msgpack_encode
        >>> from polywrap_msgpack import msgpack_decode
        >>> from polywrap_msgpack import GenericMap
        >>> msgpack_decode(msgpack_encode({"a": 1}))
        {'a': 1}
        >>> msgpack_decode(msgpack_encode(GenericMap({"a": 1})))
        GenericMap({'a': 1})
        >>> msgpack_decode(msgpack_encode([{"a": 2}, {"b": 4}]))
        [{'a': 2}, {'b': 4}]
        >>> msgpack_decode(b"\xc1")
        Traceback (most recent call last):
        ...
        polywrap_msgpack.errors.MsgpackDecodeError: Failed to decode msgpack data
    """
    try:
        return msgpack.unpackb(  # pyright: ignore[reportUnknownMemberType]
            val, ext_hook=_decode_ext_hook
        )
    except Exception as e:
        raise MsgpackDecodeError("Failed to decode msgpack data") from e


__all__ = [
    "msgpack_decode",
]
