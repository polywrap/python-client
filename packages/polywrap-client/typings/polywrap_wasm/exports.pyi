"""
This type stub file was generated by pyright.
"""

from wasmtime import Func, Instance, Store

class WrapExports:
    _instance: Instance
    _store: Store
    _wrap_invoke: Func
    def __init__(self, instance: Instance, store: Store) -> None:
        ...
    
    def __wrap_invoke__(self, method_length: int, args_length: int, env_length: int) -> bool:
        ...
    


