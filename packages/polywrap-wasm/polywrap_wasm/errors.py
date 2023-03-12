"""This module contains the error classes used by polywrap-wasm package."""
import json
from typing import Any, Dict, Optional


class WasmAbortError(RuntimeError):
    def __init__(
        self,
        uri: Optional[str],
        method: Optional[str],
        args: Optional[Dict[str, Any]],
        env: Optional[Dict[str, Any]],
        message: Optional[str],
    ):
        return super().__init__(
            f"""
            WasmWrapper: Wasm module aborted execution
            URI: {uri or "N/A"}
            Method: {method or "N/A"}
            Args: {json.dumps(dict(args), indent=2) if args else None}
            env: {json.dumps(dict(env), indent=2) if env else None}
            Message: {message or "No reason provided"}"""
        )


class ExportNotFoundError(RuntimeError):
    """raises when an export isn't found in the wasm module"""


class WasmMemoryError(RuntimeError):
    """raises when the Wasm memory is not found"""
