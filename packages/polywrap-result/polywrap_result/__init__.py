"""A simple Rust like Result type for Python 3.

This project has been forked from the https://github.com/rustedpy/result.
"""

from __future__ import annotations

import inspect
import sys
import types
from typing import (
    Any,
    Callable,
    Generic,
    NoReturn,
    TypeVar,
    Union,
    cast,
    overload,
)

if sys.version_info[:2] >= (3, 10):
    from typing import ParamSpec
else:
    from typing_extensions import ParamSpec


T_co = TypeVar("T_co", covariant=True)  # Success type
U = TypeVar("U")
F = TypeVar("F")
P = ParamSpec("P")
R = TypeVar("R")
E = TypeVar("E", bound=BaseException)


class Ok(Generic[T_co]):
    """A value that indicates success and which stores arbitrary data for the return value."""

    _value: T_co
    __match_args__ = ("value",)
    __slots__ = ("_value",)

    @overload
    def __init__(self) -> None:
        """Initialize the `Ok` type with no value.

        Raises:
            UnwrapError: If method related to `Err` is called.

        Returns:
            Ok: An instance of `Ok` type.
        """

    @overload
    def __init__(self, value: T_co) -> None:
        """Initialize the `Ok` type with a value.

        Args:
            value: The value to store.

        Raises:
            UnwrapError: If method related to `Err` is called.

        Returns:
            Ok: An instance of `Ok` type.
        """

    def __init__(self, value: Any = True) -> None:
        """Initialize the `Ok` type with a value.

        Args:
            value: The value to store.

        Raises:
            UnwrapError: If method related to `Err` is called.

        Returns:
            Ok: An instance of `Ok` type.
        """
        self._value = value

    def __repr__(self) -> str:
        """Return the representation of the `Ok` type."""
        return f"Ok({repr(self._value)})"

    def __eq__(self, other: Any) -> bool:
        """Check if the `Ok` type is equal to another `Ok` type."""
        return isinstance(other, Ok) and self.value == cast(Ok[T_co], other).value

    def __ne__(self, other: Any) -> bool:
        """Check if the `Ok` type is not equal to another `Ok` type."""
        return not self == other

    def __hash__(self) -> int:
        """Return the hash of the `Ok` type."""
        return hash((True, self._value))

    def is_ok(self) -> bool:
        """Check if the result is `Ok`."""
        return True

    def is_err(self) -> bool:
        """Check if the result is `Err`."""
        return False

    def ok(self) -> T_co:
        """Return the value."""
        return self._value

    def err(self) -> None:
        """Return `None`."""
        return None

    @property
    def value(self) -> T_co:
        """Return the inner value."""
        return self._value

    def expect(self, _message: str) -> T_co:
        """Return the value."""
        return self._value

    def expect_err(self, message: str) -> NoReturn:
        """Raise an UnwrapError since this type is `Ok`."""
        raise UnwrapError(self, message)

    def unwrap(self) -> T_co:
        """Return the value."""
        return self._value

    def unwrap_err(self) -> NoReturn:
        """Raise an UnwrapError since this type is `Ok`."""
        raise UnwrapError(self, "Called `Result.unwrap_err()` on an `Ok` value")

    def unwrap_or(self, _default: U) -> T_co:
        """Return the value."""
        return self._value

    def unwrap_or_else(self, op: Callable[[Exception], T_co]) -> T_co:
        """Return the value."""
        return self._value

    def unwrap_or_raise(self) -> T_co:
        """Return the value."""
        return self._value

    def map(self, op: Callable[[T_co], U]) -> Result[U]:
        """Return `Ok` with original value mapped to a new value using the passed in function."""
        return Ok(op(self._value))

    def map_or(self, default: U, op: Callable[[T_co], U]) -> U:
        """Return the original value mapped to a new value using the passed in function."""
        return op(self._value)

    def map_or_else(self, default_op: Callable[[], U], op: Callable[[T_co], U]) -> U:
        """Return original value mapped to a new value using the passed in `op` function."""
        return op(self._value)

    def map_err(self, op: Callable[[Exception], F]) -> Result[T_co]:
        """Return `Ok` with the original value since this type is `Ok`."""
        return cast(Result[T_co], self)

    def and_then(self, op: Callable[[T_co], Result[U]]) -> Result[U]:
        """Return the result of `op` with the original value passed in."""
        return op(self._value)

    def or_else(self, op: Callable[[Exception], Result[T_co]]) -> Result[T_co]:
        """Return `Ok` with the original value since this type is `Ok`."""
        return cast(Result[T_co], self)


class Err:
    """A value that signifies failure and which stores arbitrary data for the error."""

    __match_args__ = ("value",)
    __slots__ = ("_value",)

    def __init__(self, value: Exception) -> None:
        """Initialize the `Err` type with an exception.

        Args:
            value: The exception to store.

        Returns:
            Err: An instance of `Err` type.
        """
        self._value = value

    @classmethod
    def with_tb(cls, exc: Exception) -> "Err":
        """Create an `Err` from a string.

        Args:
            exc: The exception to store.

        Raises:
            RuntimeError: If unable to fetch the call stack frame

        Returns:
            Err: An `Err` instance
        """
        frame = inspect.currentframe()
        if not frame:
            raise RuntimeError("Unable to fetch the call stack frame!") from exc
        tb = types.TracebackType(None, frame, frame.f_lasti, frame.f_lineno)
        return cls(exc.with_traceback(tb))

    def __repr__(self) -> str:
        """Return the representation of the `Err` type."""
        return f"Err({repr(self._value)})"

    def __eq__(self, other: Any) -> bool:
        """Check if the `Err` type is equal to another `Err` type."""
        return isinstance(other, Err) and self.value == other.value

    def __ne__(self, other: Any) -> bool:
        """Check if the `Err` type is not equal to another `Err` type."""
        return not self == other

    def __hash__(self) -> int:
        """Return the hash of the `Err` type."""
        return hash((False, self._value))

    def is_ok(self) -> bool:
        """Check if the result is `Ok`."""
        return False

    def is_err(self) -> bool:
        """Check if the result is `Err`."""
        return True

    def ok(self) -> None:
        """Return `None`."""
        return None

    def err(self) -> Exception:
        """Return the error."""
        return self._value

    @property
    def value(self) -> Exception:
        """Return the inner value."""
        return self._value

    def expect(self, message: str) -> NoReturn:
        """Raise an `UnwrapError`."""
        raise UnwrapError(self, message)

    def expect_err(self, _message: str) -> Exception:
        """Return the inner value."""
        return self._value

    def unwrap(self) -> NoReturn:
        """Raise an `UnwrapError`."""
        raise UnwrapError(
            self, "Called `Result.unwrap()` on an `Err` value"
        ) from self._value

    def unwrap_err(self) -> Exception:
        """Return the inner value."""
        return self._value

    def unwrap_or(self, default: U) -> U:
        """Return `default`."""
        return default

    def unwrap_or_else(self, op: Callable[[Exception], T_co]) -> T_co:
        """Return the result of applying `op` to the error value."""
        return op(self._value)

    def unwrap_or_raise(self) -> NoReturn:
        """Raise the exception with the value of the error."""
        raise self._value

    def map(self, op: Callable[[T_co], U]) -> Result[U]:
        """Return `Err` with the same value since this type is `Err`."""
        return cast(Result[U], self)

    def map_or(self, default: U, op: Callable[[T_co], U]) -> U:
        """Return the default value since this type is `Err`."""
        return default

    def map_or_else(self, default_op: Callable[[], U], op: Callable[[T_co], U]) -> U:
        """Return the result of the default operation since this type is `Err`."""
        return default_op()

    def map_err(self, op: Callable[[Exception], Exception]) -> Result[T_co]:
        """Return `Err` with original error mapped to a new value using the passed in function."""
        return Err(op(self._value))

    def and_then(self, op: Callable[[T_co], Result[U]]) -> Result[U]:
        """Return `Err` with the original value since this type is `Err`."""
        return cast(Result[U], self)

    def or_else(self, op: Callable[[Exception], Result[T_co]]) -> Result[T_co]:
        """Return the result of `op` with the original value passed in."""
        return op(self._value)


# A simple `Result` type inspired by Rust.
# Not all methods (https://doc.rust-lang.org/std/result/enum.Result.html)
# have been implemented, only the ones that make sense in the Python context.
Result = Union[Ok[T_co], Err]


class UnwrapError(Exception):
    """
    Exception raised from ``.unwrap_<...>`` and ``.expect_<...>`` calls.

    The original ``Result`` can be accessed via the ``.result`` attribute, but
    this is not intended for regular use, as type information is lost:
    ``UnwrapError`` doesn't know about both ``T`` and ``E``, since it's raised
    from ``Ok()`` or ``Err()`` which only knows about either ``T`` or ``E``,
    not both.
    """

    _result: Result[Any]

    def __init__(self, result: Result[Any], message: str) -> None:
        """Initialize the `UnwrapError` type.

        Args:
            result: The original result.
            message: The error message.

        Returns:
            UnwrapError: An instance of `UnwrapError` type.
        """
        self._result = result
        super().__init__(message)

    @property
    def result(self) -> Result[Any]:
        """Return the original result."""
        return self._result
