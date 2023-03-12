"""This module contains the State type for holding the state of a Wasm wrapper."""
from dataclasses import dataclass, field
from typing import Any, List, Optional, TypedDict


class RawInvokeResult(TypedDict):
    """The result of an invoke call.
    
    Attributes:
        result: The result of the invoke call or none if error.
        error: The error of the invoke call or none if result.
    """
    result: Optional[bytes]
    error: Optional[str]


class RawSubinvokeResult(TypedDict):
    """The result of a subinvoke call.
    
    Attributes:
        result: The result of the subinvoke call or none if error.
        error: The error of the subinvoke call or none if result.
        args: The arguments of the subinvoke call.
    """
    result: Optional[bytes]
    error: Optional[str]
    args: List[Any]


class RawSubinvokeImplementationResult(TypedDict):
    """The result of a subinvoke implementation call.

    Attributes:
        result: The result of the subinvoke implementation call or none if error.
        error: The error of the subinvoke implementation call or none if result.
        args: The arguments of the subinvoke implementation call.
    """
    result: Optional[bytes]
    error: Optional[str]
    args: List[Any]


@dataclass(kw_only=True, slots=True)
class State:
    """State is a dataclass that holds the state of a Wasm wrapper.

    Attributes:
        raw_invoke_result: The result of an invocation.
        raw_subinvoke_result: The result of a subinvocation.
        raw_subinvoke_implementation_result: The result of a subinvoke implementation call.
        get_implementations_result: The result of a get implementations call.
        method: The method of the invoke call.
        args: The arguments of the invoke call.
        env: The environment of the invoke call.
    """
    invoke: RawInvokeResult = field(
        default_factory=lambda: {"result": None, "error": None}
    )
    subinvoke: RawSubinvokeResult = field(
        default_factory=lambda: {"result": None, "error": None, "args": []}
    )
    subinvoke_implementation: RawSubinvokeImplementationResult = field(
        default_factory=lambda: {"result": None, "error": None, "args": []}
    )
    get_implementations_result: Optional[bytes] = None
    method: Optional[str] = None
    args: Optional[bytes] = None
    env: Optional[bytes] = None
