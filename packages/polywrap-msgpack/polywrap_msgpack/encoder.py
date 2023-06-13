"""This module implements the msgpack encoder for encoding data \
    before sending it to a wrapper."""
from __future__ import annotations

from typing import Any, cast

import msgpack
from msgpack.ext import ExtType

from .errors import MsgpackEncodeError, MsgpackExtError, MsgpackSanitizeError
from .extensions import ExtensionTypes, GenericMap
from .sanitize import sanitize


def _encode_ext_hook(obj: Any) -> ExtType:
    """Extension hook for extending the msgpack supported types.

    Args:
        obj (Any): object to be encoded

    Raises:
        MsgpackExtError: when given object is not a supported extension type

    Returns:
        Tuple[int, bytes]: extension type code and payload
    """
    if isinstance(obj, GenericMap):
        return ExtType(
            ExtensionTypes.GENERIC_MAP.value,
            # pylint: disable=protected-access
            msgpack_encode(
                cast(
                    GenericMap[Any, Any], obj
                )._map  # pyright: ignore[reportPrivateUsage]
            ),
        )
    raise MsgpackExtError(f"Object of type {type(obj)} is not supported")


def msgpack_encode(value: Any) -> bytes:
    r"""Encode any python object into msgpack bytes.

    Args:
        value (Any): any valid python object

    Raises:
        MsgpackExtError: when given object is not a supported extension type
        MsgpackEncodeError: when sanitized object is not msgpack serializable
        MsgpackSanitizeError: when given object is not sanitizable

    Returns:
        bytes: encoded msgpack value

    Examples:
        >>> from polywrap_msgpack import msgpack_encode
        >>> from polywrap_msgpack import msgpack_decode
        >>> from polywrap_msgpack import GenericMap
        >>> msgpack_encode({"a": 1})
        b'\x81\xa1a\x01'
        >>> msgpack_encode(GenericMap({"a": 1}))
        b'\xd6\x01\x81\xa1a\x01'
        >>> msgpack_encode({1.0: 1})
        Traceback (most recent call last):
        ...
        polywrap_msgpack.errors.MsgpackSanitizeError: Failed to sanitize object
    """
    try:
        sanitized = sanitize(value)
    except Exception as e:
        raise MsgpackSanitizeError("Failed to sanitize object") from e

    try:
        return msgpack.packb(sanitized, default=_encode_ext_hook, use_bin_type=True)
    except Exception as e:
        raise MsgpackEncodeError("Failed to encode object") from e


__all__ = [
    "msgpack_encode",
]
