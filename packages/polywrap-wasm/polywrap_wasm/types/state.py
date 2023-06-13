"""This module contains the State type for holding the state of a Wasm wrapper."""
from dataclasses import dataclass
from typing import Any, Generic, Optional, TypeVar

from polywrap_core import Uri, UriResolutionContext

E = TypeVar("E")


@dataclass(kw_only=True, slots=True)
class WasmInvokeOptions:
    """WasmInvokeOptions is a dataclass that holds the options for an invocation.

    Args:
        uri: The URI of the wrapper.
        method: The method to invoke.
        args: The arguments to pass to the method.
        env: The environment variables to set for the invocation.
        resolution_context: A URI resolution context.
    """

    uri: Uri
    method: str
    args: Optional[dict[str, Any]] = None
    env: Optional[dict[str, Any]] = None
    resolution_context: Optional[UriResolutionContext] = None


@dataclass(kw_only=True, slots=True)
class InvokeResult(Generic[E]):
    """InvokeResult is a dataclass that holds the result of an invocation.

    Args:
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

    Args:
        invoke_options: The options used for the invocation.
        invoke_result: The result of an invocation.
        subinvoke_result: The result of a subinvocation.
        subinvoke_implementation_result: The result of a subinvoke implementation invoke call.
        get_implementations_result: The result of a get implementations call.
    """

    invoke_options: WasmInvokeOptions
    invoke_result: Optional[InvokeResult[str]] = None
    subinvoke_result: Optional[InvokeResult[Exception]] = None
    get_implementations_result: Optional[bytes] = None
