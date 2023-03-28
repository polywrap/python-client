"""This module contains the State type for holding the state of a Wasm wrapper."""
from dataclasses import dataclass
from typing import Generic, Optional, TypeVar

from polywrap_core import InvokeOptions, UriPackageOrWrapper

E = TypeVar("E")


@dataclass(kw_only=True, slots=True)
class InvokeResult(Generic[E]):
    """InvokeResult is a dataclass that holds the result of an invocation.

    Attributes:
        result: The result of an invocation.
        error: The error of an invocation.
    """

    result: Optional[bytes] = None
    error: Optional[E] = None

    def __post_init__(self):
        """Validate that either result or error is set."""
        if self.result is None and self.error is None:
            raise ValueError(
                "Either result or error must be set in InvokeResult instance."
            )


@dataclass(kw_only=True, slots=True)
class State:
    """State is a dataclass that holds the state of a Wasm wrapper.

    Attributes:
        invoke_options: The options used for the invocation.
        invoke_result: The result of an invocation.
        subinvoke_result: The result of a subinvocation.
        subinvoke_implementation_result: The result of a subinvoke implementation invoke call.
        get_implementations_result: The result of a get implementations call.
    """

    invoke_options: InvokeOptions[UriPackageOrWrapper]
    invoke_result: Optional[InvokeResult[str]] = None
    subinvoke_result: Optional[InvokeResult[Exception]] = None
    get_implementations_result: Optional[bytes] = None
