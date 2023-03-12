"""This module contains the error classes used by polywrap-wasm package."""
class WasmAbortError(RuntimeError):
    def __init__(self, message: str):
        return super().__init__(
            f"""
            WasmWrapper: Wasm module aborted execution
            URI:
            Method:
            Args:
            Message: {message}"""
        )


class ExportNotFoundError(RuntimeError):
    """raises when an export isn't found in the wasm module"""


class WasmMemoryError(RuntimeError):
    """raises when the Wasm memory is not found"""