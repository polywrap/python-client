"""This module implements the msgpack encoder for encoding data \
    before sending it to a wrapper."""
from __future__ import annotations

from typing import Any, cast

import msgpack
from msgpack.ext import ExtType

from .errors import MsgpackEncodeError, MsgpackExtError, MsgpackSanitizeError
from .extensions import ExtensionTypes, GenericMap
from .sanitize import sanitize


def encode_ext_hook(obj: Any) -> ExtType:
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
            msgpack_encode(cast(GenericMap[Any, Any], obj)._map),
        )  # pyright: reportPrivateUsage=false
    raise MsgpackExtError(f"Object of type {type(obj)} is not supported")


def msgpack_encode(value: Any) -> bytes:
    """Encode any python object into msgpack bytes.

    Args:
        value (Any): any valid python object

    Raises:
        MsgpackEncodeError: when sanitized object is not msgpack serializable
        MsgpackSanitizeError: when given object is not sanitizable

    Returns:
        bytes: encoded msgpack value
    """
    try:
        sanitized = sanitize(value)
    except Exception as e:
        raise MsgpackSanitizeError("Failed to sanitize object") from e

    try:
        return msgpack.packb(sanitized, default=encode_ext_hook, use_bin_type=True)
    except Exception as e:
        raise MsgpackEncodeError("Failed to encode object") from e
