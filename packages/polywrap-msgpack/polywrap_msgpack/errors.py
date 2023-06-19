"""This module contains Errors for the polywrap-msgpack package."""


class MsgpackError(Exception):
    """Base class for all exceptions in this module."""


class MsgpackDecodeError(MsgpackError):
    """Raised when there is an error decoding a msgpack object."""


class MsgpackEncodeError(MsgpackError):
    """Raised when there is an error encoding a msgpack object."""


class MsgpackExtError(MsgpackError):
    """Raised when there is an error with a msgpack extension."""


class MsgpackSanitizeError(MsgpackError):
    """Raised when there is an error sanitizing a python object\
        into a msgpack encoder compatible format."""


__all__ = [
    "MsgpackError",
    "MsgpackDecodeError",
    "MsgpackEncodeError",
    "MsgpackExtError",
    "MsgpackSanitizeError",
]
