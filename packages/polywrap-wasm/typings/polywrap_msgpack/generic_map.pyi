"""
This type stub file was generated by pyright.
"""

from typing import Dict, MutableMapping, TypeVar

"""This module contains GenericMap implementation for msgpack extention type."""
K = TypeVar("K")
V = TypeVar("V")
class GenericMap(MutableMapping[K, V]):
    """GenericMap is a type that can be used to represent generic map extention type in msgpack."""
    _map: Dict[K, V]
    def __init__(self, _map: MutableMapping[K, V]) -> None:
        """Initialize the key - value mapping.

        Args:
            map: A dictionary of keys and values to be used for
        """
        ...
    
    def has(self, key: K) -> bool:
        """Check if the map contains the key.

        Args:
            key: The key to look up. It must be a key in the mapping.

        Returns:
            True if the key is in the map, False otherwise
        """
        ...
    
    def __getitem__(self, key: K) -> V:
        """Return the value associated with the key.

        Args:
            key: The key to look up. It must be a key in the mapping.

        Returns:
            The value associated with the key or None if
            the key doesn't exist in the dictionary or is out of range
        """
        ...
    
    def __setitem__(self, key: K, value: V) -> None:
        """Set the value associated with the key.

        Args:
            key: The key to set.
        value: The value to set.
        """
        ...
    
    def __delitem__(self, key: K) -> None:
        """Delete an item from the map.

        Args:
            key: key of the item to delete.
        """
        ...
    
    def __iter__(self): # -> Iterator[K@GenericMap]:
        """Iterate over the keys in the map.

        Returns:
            An iterator over the keys in the map.
        """
        ...
    
    def __len__(self) -> int:
        """Return the number of elements in the map.

        Returns:
            The number of elements in the map as an integer ( 0 or greater ).
        """
        ...
    
    def __repr__(self) -> str:
        """Return a string representation of the GenericMap. This is useful for debugging purposes.

        Returns:
            A string representation of the GenericMap ( including the name of the map ).
        """
        ...
    

