from typing import Any, Dict, TypeVar, Generic

TConfig = TypeVar('TConfig')

class PluginModule(TConfig):
    env: Dict[str, Any]
    config: TConfig

    def __init__(self, env: Dict[str, Any], config: TConfig):
        pass
