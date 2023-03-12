"""This module contains the error classes used by polywrap-wasm package."""
import json
from typing import Any, Dict, Optional


class WasmAbortError(RuntimeError):
    """Raises when the Wasm module aborts execution.

    Attributes:
        uri: The uri of the wrapper that is being invoked.
        method: The method of the wrapper that is being invoked.
        args: The arguments for the wrapper method that is being invoked.
        env: The environment variables of the wrapper that is being invoked.
        message: The message provided by the Wasm module.
    """

    uri: Optional[str]
    method: Optional[str]
    arguments: Optional[Dict[str, Any]]
    env: Optional[Dict[str, Any]]
    message: Optional[str]

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        uri: Optional[str],
        method: Optional[str],
        args: Optional[Dict[str, Any]],
        env: Optional[Dict[str, Any]],
        message: Optional[str],
    ):
        """Initialize a new instance of WasmAbortError."""
        self.uri = uri
        self.method = method
        self.arguments = args
        self.env = env
        self.message = message

        super().__init__(
            f"""
            WasmWrapper: Wasm module aborted execution
            URI: {uri or "N/A"}
            Method: {method or "N/A"}
            Args: {json.dumps(dict(args), indent=2) if args else None}
            env: {json.dumps(dict(env), indent=2) if env else None}
            Message: {message or "No reason provided"}"""
        )


class ExportNotFoundError(RuntimeError):
    """Raises when an export isn't found in the wasm module."""


class WasmMemoryError(RuntimeError):
    """Raises when the Wasm memory is not found."""
