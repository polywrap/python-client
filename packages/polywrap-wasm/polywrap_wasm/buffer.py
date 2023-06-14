"""This module provides a set of functions to read and write bytes from a memory buffer."""
# pylint: disable=protected-access

import ctypes
from typing import TYPE_CHECKING, Any, Optional  # pyright: ignore[reportUnusedImport]

BufferPointer = (
    ctypes._Pointer[ctypes.c_ubyte]  # pyright: ignore[reportPrivateUsage]
    if TYPE_CHECKING
    else Any
)


def read_bytes(
    memory_pointer: BufferPointer,
    memory_length: int,
    offset: Optional[int] = None,
    length: Optional[int] = None,
) -> bytes:
    """Read bytes from a memory buffer.

    Args:
        memory_pointer (BufferPointer): The pointer to the memory buffer.
        memory_length (int): The length of the memory buffer.
        offset (Optional[int]): The offset to start reading from.
        length (Optional[int]): The number of bytes to read.
    """
    result = bytearray(memory_length)
    buffer = (ctypes.c_ubyte * memory_length).from_buffer(result)
    ctypes.memmove(buffer, memory_pointer, memory_length)

    return bytes(result[offset : offset + length] if offset and length else result)


def read_string(
    memory_pointer: BufferPointer, memory_length: int, offset: int, length: int
) -> str:
    """Read a UTF-8 encoded string from a memory buffer.

    Args:
        memory_pointer (BufferPointer): The pointer to the memory buffer.
        memory_length (int): The length of the memory buffer.
        offset (int): The offset to start reading from.
        length (int): The number of bytes to read.
    """
    value = read_bytes(memory_pointer, memory_length, offset, length)
    return value.decode("utf-8")


def write_bytes(
    memory_pointer: BufferPointer,
    memory_length: int,
    value: bytes,
    value_offset: int,
) -> None:
    """Write bytes to a memory buffer.

    Args:
        memory_pointer (BufferPointer): The pointer to the memory buffer.
        memory_length (int): The length of the memory buffer.
        value (bytes): The bytes to write.
        value_offset (int): The offset to start writing to.
    """
    mem_cpy(memory_pointer, memory_length, bytearray(value), len(value), value_offset)


def write_string(
    memory_pointer: BufferPointer,
    memory_length: int,
    value: str,
    value_offset: int,
) -> None:
    """Write a UTF-8 encoded string to a memory buffer.

    Args:
        memory_pointer (BufferPointer): The pointer to the memory buffer.
        memory_length (int): The length of the memory buffer.
        value (str): The string to write.
        value_offset (int): The offset to start writing to.
    """
    value_buffer = value.encode("utf-8")
    write_bytes(
        memory_pointer,
        memory_length,
        value_buffer,
        value_offset,
    )


def mem_cpy(
    memory_pointer: BufferPointer,
    memory_length: int,
    value: bytearray,
    value_length: int,
    value_offset: int,
) -> None:
    """Copy bytearray from the given value to a memory buffer.

    Args:
        memory_pointer (BufferPointer): The pointer to the memory buffer.
        memory_length (int): The length of the memory buffer.
        value (bytearray): The bytearray to copy.
        value_length (int): The length of the bytearray to copy.
        value_offset (int): The offset to start copying from.
    """
    current_value = bytearray(
        read_bytes(
            memory_pointer,
            memory_length,
        )
    )

    new_value = (ctypes.c_ubyte * value_length).from_buffer(value)
    current_value[value_offset : value_offset + value_length] = new_value

    current_value_buffer = (ctypes.c_ubyte * memory_length).from_buffer(current_value)
    ctypes.memmove(memory_pointer, current_value_buffer, memory_length)
