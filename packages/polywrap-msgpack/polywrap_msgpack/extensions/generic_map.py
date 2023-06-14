"""This module contains GenericMap implementation for msgpack extension type."""
from typing import Dict, Iterator, MutableMapping, TypeVar

K = TypeVar("K")
V = TypeVar("V")


class GenericMap(MutableMapping[K, V]):
    """GenericMap is a type that can be used to represent generic map extension type in msgpack.

    Examples:
        >>> from polywrap_msgpack import GenericMap
        >>> GenericMap({1: 2, 3: 4})
        GenericMap({1: 2, 3: 4})
        >>> map = GenericMap({1: 2, 3: 4})
        >>> map[5] = 6
        >>> map
        GenericMap({1: 2, 3: 4, 5: 6})
        >>> map[7]
        Traceback (most recent call last):
        ...
        KeyError: 7
        >>> 7 in map
        False
        >>> 1 in map
        True
        >>> len(map)
        3
        >>> del map[1]
        >>> map
        GenericMap({3: 4, 5: 6})
        >>> del map[7]
        Traceback (most recent call last):
        ...
        KeyError: 7
    """

    _map: Dict[K, V]

    def __init__(self, _map: MutableMapping[K, V]):
        """Initialize the key - value mapping.

        Args:
            map: A dictionary of keys and values to be used for
        """
        self._map = dict(_map)

    def __contains__(self, key: object) -> bool:
        """Check if the map contains the key.

        Args:
            key: The key to look up. It must be a key in the mapping.

        Returns:
            True if the key is in the map, False otherwise
        """
        return key in self._map

    def __getitem__(self, key: K) -> V:
        """Return the value associated with the key.

        Args:
            key: The key to look up. It must be a key in the mapping.

        Raises:
            KeyError: If the key is not in the map.

        Returns:
            The value associated with the key or None if
            the key doesn't exist in the dictionary or is out of range
        """
        return self._map[key]

    def __setitem__(self, key: K, value: V) -> None:
        """Set the value associated with the key.

        Args:
            key: The key to set.
            value: The value to set.
        """
        self._map[key] = value

    def __delitem__(self, key: K) -> None:
        """Delete an item from the map.

        Args:
            key: key of the item to delete.

        Raises:
            KeyError: If the key is not in the map.
        """
        del self._map[key]

    def __iter__(self) -> Iterator[K]:
        """Iterate over the keys in the map.

        Returns:
            An iterator over the keys in the map.
        """
        return iter(self._map)

    def __len__(self) -> int:
        """Return the number of elements in the map.

        Returns:
            The number of elements in the map as an integer ( 0 or greater ).
        """
        return len(self._map)

    def __repr__(self) -> str:
        """Return a string representation of the GenericMap. This is useful for debugging purposes.

        Returns:
            A string representation of the GenericMap ( including the name of the map ).
        """
        return f"GenericMap({repr(self._map)})"
