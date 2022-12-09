"""
A simple Rust like Result type for Python 3.

This project has been forked from the https://github.com/rustedpy/result.
"""

from __future__ import annotations

import inspect
import sys
import types
from typing import Any, Callable, Generic, NoReturn, TypeVar, Union, cast, overload

if sys.version_info[:2] >= (3, 10):
    from typing import ParamSpec
else:
    from typing_extensions import ParamSpec


T = TypeVar("T", covariant=True)  # Success type
U = TypeVar("U")
F = TypeVar("F")
P = ParamSpec("P")
R = TypeVar("R")
TBE = TypeVar("TBE", bound=BaseException)


class Ok(Generic[T]):
    """
    A value that indicates success and which stores arbitrary data for the return value.
    """

    _value: T
    __match_args__ = ("value",)
    __slots__ = ("_value",)

    @overload
    def __init__(self) -> None:
        ...  # pragma: no cover

    @overload
    def __init__(self, value: T) -> None:
        ...  # pragma: no cover

    def __init__(self, value: Any = True) -> None:
        self._value = value

    def __repr__(self) -> str:
        return f"Ok({repr(self._value)})"

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Ok) and self.value == cast(Ok[T], other).value

    def __ne__(self, other: Any) -> bool:
        return not self == other

    def __hash__(self) -> int:
        return hash((True, self._value))

    def is_ok(self) -> bool:
        return True

    def is_err(self) -> bool:
        return False

    def ok(self) -> T:
        """
        Return the value.
        """
        return self._value

    def err(self) -> None:
        """
        Return `None`.
        """
        return None

    @property
    def value(self) -> T:
        """
        Return the inner value.
        """
        return self._value

    def expect(self, _message: str) -> T:
        """
        Return the value.
        """
        return self._value

    def expect_err(self, message: str) -> NoReturn:
        """
        Raise an UnwrapError since this type is `Ok`
        """
        raise UnwrapError(self, message)

    def unwrap(self) -> T:
        """
        Return the value.
        """
        return self._value

    def unwrap_err(self) -> NoReturn:
        """
        Raise an UnwrapError since this type is `Ok`
        """
        raise UnwrapError(self, "Called `Result.unwrap_err()` on an `Ok` value")

    def unwrap_or(self, _default: U) -> T:
        """
        Return the value.
        """
        return self._value

    def unwrap_or_else(self, op: Callable[[Exception], T]) -> T:
        """
        Return the value.
        """
        return self._value

    def unwrap_or_raise(self) -> T:
        """
        Return the value.
        """
        return self._value

    def map(self, op: Callable[[T], U]) -> Result[U]:
        """
        The contained result is `Ok`, so return `Ok` with original value mapped to
        a new value using the passed in function.
        """
        return Ok(op(self._value))

    def map_or(self, default: U, op: Callable[[T], U]) -> U:
        """
        The contained result is `Ok`, so return the original value mapped to a new
        value using the passed in function.
        """
        return op(self._value)

    def map_or_else(self, default_op: Callable[[], U], op: Callable[[T], U]) -> U:
        """
        The contained result is `Ok`, so return original value mapped to
        a new value using the passed in `op` function.
        """
        return op(self._value)

    def map_err(self, op: Callable[[Exception], F]) -> Result[T]:
        """
        The contained result is `Ok`, so return `Ok` with the original value
        """
        return cast(Result[T], self)

    def and_then(self, op: Callable[[T], Result[U]]) -> Result[U]:
        """
        The contained result is `Ok`, so return the result of `op` with the
        original value passed in
        """
        return op(self._value)

    def or_else(self, op: Callable[[Exception], Result[T]]) -> Result[T]:
        """
        The contained result is `Ok`, so return `Ok` with the original value
        """
        return cast(Result[T], self)


class Err:
    """
    A value that signifies failure and which stores arbitrary data for the error.
    """

    __match_args__ = ("value",)
    __slots__ = ("_value",)

    def __init__(self, value: Exception) -> None:
        self._value = value

    @classmethod
    def from_str(cls, value: str) -> "Err":
        frame = inspect.currentframe()
        if not frame:
            raise RuntimeError("Unable to fetch the call stack frame!")
        tb = types.TracebackType(None, frame, frame.f_lasti, frame.f_lineno)
        return cls(Exception(value).with_traceback(tb))

    def __repr__(self) -> str:
        return f"Err({repr(self._value)})"

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Err) and self.value == other.value

    def __ne__(self, other: Any) -> bool:
        return not self == other

    def __hash__(self) -> int:
        return hash((False, self._value))

    def is_ok(self) -> bool:
        return False

    def is_err(self) -> bool:
        return True

    def ok(self) -> None:
        """
        Return `None`.
        """
        return None

    def err(self) -> Exception:
        """
        Return the error.
        """
        return self._value

    @property
    def value(self) -> Exception:
        """
        Return the inner value.
        """
        return self._value

    def expect(self, message: str) -> NoReturn:
        """
        Raises an `UnwrapError`.
        """
        raise UnwrapError(self, message)

    def expect_err(self, _message: str) -> Exception:
        """
        Return the inner value
        """
        return self._value

    def unwrap(self) -> NoReturn:
        """
        Raises an `UnwrapError`.
        """
        raise UnwrapError(
            self, "Called `Result.unwrap()` on an `Err` value"
        ) from self._value

    def unwrap_err(self) -> Exception:
        """
        Return the inner value
        """
        return self._value

    def unwrap_or(self, default: U) -> U:
        """
        Return `default`.
        """
        return default

    def unwrap_or_else(self, op: Callable[[Exception], T]) -> T:
        """
        The contained result is ``Err``, so return the result of applying
        ``op`` to the error value.
        """
        return op(self._value)

    def unwrap_or_raise(self) -> NoReturn:
        """
        The contained result is ``Err``, so raise the exception with the value.
        """
        raise self._value

    def map(self, op: Callable[[T], U]) -> Result[U]:
        """
        Return `Err` with the same value
        """
        return cast(Result[U], self)

    def map_or(self, default: U, op: Callable[[T], U]) -> U:
        """
        Return the default value
        """
        return default

    def map_or_else(self, default_op: Callable[[], U], op: Callable[[T], U]) -> U:
        """
        Return the result of the default operation
        """
        return default_op()

    def map_err(self, op: Callable[[Exception], Exception]) -> Result[T]:
        """
        The contained result is `Err`, so return `Err` with original error mapped to
        a new value using the passed in function.
        """
        return Err(op(self._value))

    def and_then(self, op: Callable[[T], Result[U]]) -> Result[U]:
        """
        The contained result is `Err`, so return `Err` with the original value
        """
        return cast(Result[U], self)

    def or_else(self, op: Callable[[Exception], Result[T]]) -> Result[T]:
        """
        The contained result is `Err`, so return the result of `op` with the
        original value passed in
        """
        return op(self._value)


# define Result as a generic type alias for use
# in type annotations
"""
A simple `Result` type inspired by Rust.
Not all methods (https://doc.rust-lang.org/std/result/enum.Result.html)
have been implemented, only the ones that make sense in the Python context.
"""
Result = Union[Ok[T], Err]


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
        self._result = result
        super().__init__(message)

    @property
    def result(self) -> Result[Any]:
        """
        Returns the original result.
        """
        return self._result
