from typing import Dict, MutableMapping, TypeVar

K = TypeVar("K")
V = TypeVar("V")


class GenericMap(MutableMapping[K, V]):
    _map: Dict[K, V]

    def __init__(self, map: Dict[K, V]):
        self._map = dict(map)

    def __getitem__(self, key: K) -> V:
        return self._map[key]

    def __setitem__(self, key: K, value: V) -> None:
        self._map[key] = value

    def __delitem__(self, key: K) -> None:
        del self._map[key]

    def __iter__(self):
        return iter(self._map)

    def __len__(self) -> int:
        return len(self._map)

    def __repr__(self) -> str:
        return f"GenericMap({repr(self._map)})"
