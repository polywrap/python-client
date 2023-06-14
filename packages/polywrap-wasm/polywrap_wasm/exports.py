"""This module contains the exports of the Wasm wrapper module."""
from wasmtime import Func, Instance, Store

from .errors import WasmExportNotFoundError


class WrapExports:
    """WrapExports is a class that contains the exports of the Wasm wrapper module.

    Args:
        instance (Instance): The Wasm instance.
        store (Store): The Wasm store.
        _wrap_invoke (Func): The exported _wrap_invoke Wasm function.

    Raises:
        WasmExportNotFoundError: If the _wrap_invoke function is not exported\
            from the Wasm module.
    """

    _instance: Instance
    _store: Store
    _wrap_invoke: Func

    def __init__(self, instance: Instance, store: Store):
        """Initialize the WrapExports class."""
        self._instance = instance
        self._store = store
        exports = instance.exports(store)
        _wrap_invoke = exports.get("_wrap_invoke")
        if not _wrap_invoke or not isinstance(_wrap_invoke, Func):
            raise WasmExportNotFoundError(
                "Expected _wrap_invoke to be exported from the Wasm module."
            )
        self._wrap_invoke = _wrap_invoke

    def __wrap_invoke__(
        self, method_length: int, args_length: int, env_length: int
    ) -> bool:
        """Call the exported _wrap_invoke Wasm function.

        Args:
            method_length (int): The length of the method.
            args_length (int): The length of the args.
            env_length (int): The length of the env.

        Returns:
            True if the invoke call was successful, False otherwise.
        """
        return bool(
            self._wrap_invoke(self._store, method_length, args_length, env_length)
        )
