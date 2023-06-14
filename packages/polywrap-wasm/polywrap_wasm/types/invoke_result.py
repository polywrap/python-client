"""This module contains the InvokeResult type."""
from dataclasses import dataclass
from typing import Generic, Optional, TypeVar

E = TypeVar("E")


@dataclass(kw_only=True, slots=True)
class InvokeResult(Generic[E]):
    """InvokeResult is a dataclass that holds the result of an invocation.

    Args:
        result (Optional[bytes]): The result of an invocation.
        error (Optional[E]): The error of an invocation.
    """

    result: Optional[bytes] = None
    error: Optional[E] = None

    def __post_init__(self):
        """Validate that either result or error is set."""
        if self.result is None and self.error is None:
            raise ValueError(
                "Either result or error must be set in InvokeResult instance."
            )
