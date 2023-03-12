"""This module contains the exports of the Wasm wrapper module."""
from wasmtime import Func, Instance, Store

from .errors import ExportNotFoundError


class WrapExports:
    """WrapExports is a class that contains the exports of the Wasm wrapper module.
    
    Attributes:
        _instance: The Wasm instance.
        _store: The Wasm store.
        _wrap_invoke: exported _wrap_invoke Wasm function.
    """
    _instance: Instance
    _store: Store
    _wrap_invoke: Func

    def __init__(self, instance: Instance, store: Store):
        """Initializes the WrapExports class.
        
        Args:
            instance: The Wasm instance.
            store: The Wasm store.
        
        Raises:
            ExportNotFoundError: if the _wrap_invoke export is not found in the Wasm module.
        """
        self._instance = instance
        self._store = store
        exports = instance.exports(store)
        _wrap_invoke = exports.get("_wrap_invoke")
        if not _wrap_invoke or not isinstance(_wrap_invoke, Func):
            raise ExportNotFoundError(
                "Unable to find exported wasm module function: _wrap_invoke in the module"
            )
        self._wrap_invoke = _wrap_invoke

    def __wrap_invoke__(
        self, method_length: int, args_length: int, env_length: int
    ) -> bool:
        """Calls the exported _wrap_invoke Wasm function.

        Args:
            method_length: The length of the method.
            args_length: The length of the args.
            env_length: The length of the env.

        Returns:
            True if the invoke call was successful, False otherwise.
        """
        return bool(
            self._wrap_invoke(self._store, method_length, args_length, env_length)
        )
