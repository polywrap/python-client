"""This module contains the State type for holding the state of a Wasm wrapper."""
from dataclasses import dataclass
from typing import Optional

from polywrap_result import Result


@dataclass(kw_only=True, slots=True)
class State:
    """State is a dataclass that holds the state of a Wasm wrapper.

    Attributes:
        invoke_result: The result of an invocation.
        subinvoke_result: The result of a subinvocation.
        subinvoke_implementation_result: The result of a subinvoke implementation call.
        get_implementations_result: The result of a get implementations call.
        uri: The uri of the wrapper that is being invoked.
        method: The method of the wrapper that is being invoked.
        args: The arguments for the wrapper method that is being invoked.
        env: The environment variables of the wrapper that is being invoked.
    """

    invoke_result: Optional[Result[bytes]] = None
    subinvoke_result: Optional[Result[bytes]] = None
    subinvoke_implementation_result: Optional[Result[bytes]] = None
    get_implementations_result: Optional[bytes] = None
    uri: Optional[str] = None
    method: Optional[str] = None
    args: Optional[bytes] = None
    env: Optional[bytes] = None
