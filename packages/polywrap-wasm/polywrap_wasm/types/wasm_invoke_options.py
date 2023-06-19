"""This module contains the InvokeOptions type for a Wasm wrapper."""
from dataclasses import dataclass
from typing import Any, Optional

from polywrap_core import Uri, UriResolutionContext


@dataclass(kw_only=True, slots=True)
class WasmInvokeOptions:
    """WasmInvokeOptions is a dataclass that holds the options for an invocation.

    Args:
        uri (Uri): The URI of the wrapper.
        method (str): The method to invoke.
        args (Optional[dict[str, Any]]): The arguments to pass to the method.
        env (Optional[dict[str, Any]]): The environment variables to set\
            for the invocation.
        resolution_context (Optional[UriResolutionContext]): \
            A URI resolution context.
    """

    uri: Uri
    method: str
    args: Optional[dict[str, Any]] = None
    env: Optional[dict[str, Any]] = None
    resolution_context: Optional[UriResolutionContext] = None
