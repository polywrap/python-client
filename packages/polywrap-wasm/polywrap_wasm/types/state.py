"""This module contains the State type for holding the state of a Wasm wrapper."""
from dataclasses import dataclass
from typing import Optional

from .invoke_result import InvokeResult
from .wasm_invoke_options import WasmInvokeOptions


@dataclass(kw_only=True, slots=True)
class State:
    """State is a dataclass that holds the state of a Wasm wrapper.

    Args:
        invoke_options (WasmInvokeOptions): \
            The options used for the invocation.
        invoke_result (Optional[InvokeResult[str]]): \
            The result of an invocation.
        subinvoke_result (Optional[InvokeResult[Exception]]): \
            The result of a subinvocation.
        get_implementations_result (Optional[bytes]) : \
            The result of a get implementations call.
    """

    invoke_options: WasmInvokeOptions
    invoke_result: Optional[InvokeResult[str]] = None
    subinvoke_result: Optional[InvokeResult[Exception]] = None
    get_implementations_result: Optional[bytes] = None
