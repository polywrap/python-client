"""This module provides a set of functions to read and write bytes from a memory buffer."""
import ctypes
from typing import TYPE_CHECKING, Any, Optional  # pyright: ignore[reportUnusedImport]

BufferPointer = ctypes._Pointer[ctypes.c_ubyte] if TYPE_CHECKING else Any  # type: ignore


def read_bytes(
    memory_pointer: BufferPointer,
    memory_length: int,
    offset: Optional[int] = None,
    length: Optional[int] = None,
) -> bytearray:
    """Reads bytes from a memory buffer.
    
    Args:
        memory_pointer: The pointer to the memory buffer.
        memory_length: The length of the memory buffer.
        offset: The offset to start reading from.
        length: The number of bytes to read.
    """
    result = bytearray(memory_length)
    buffer = (ctypes.c_ubyte * memory_length).from_buffer(result)
    ctypes.memmove(buffer, memory_pointer, memory_length)

    return result[offset : offset + length] if offset and length else result


def read_string(
    memory_pointer: BufferPointer, memory_length: int, offset: int, length: int
) -> str:
    """Reads a UTF-8 encoded string from a memory buffer.
    
    Args:
        memory_pointer: The pointer to the memory buffer.
        memory_length: The length of the memory buffer.
        offset: The offset to start reading from.
        length: The number of bytes to read.
    """
    value = read_bytes(memory_pointer, memory_length, offset, length)
    return value.decode("utf-8")


def write_bytes(
    memory_pointer: BufferPointer,
    memory_length: int,
    value: bytes,
    value_offset: int,
) -> None:
    """Writes bytes to a memory buffer.
    
    Args:
        memory_pointer: The pointer to the memory buffer.
        memory_length: The length of the memory buffer.
        value: The bytes to write.
        value_offset: The offset to start writing to.
    """
    mem_cpy(memory_pointer, memory_length, bytearray(value), len(value), value_offset)


def write_string(
    memory_pointer: BufferPointer,
    memory_length: int,
    value: str,
    value_offset: int,
) -> None:
    """Writes a UTF-8 encoded string to a memory buffer.
    
    Args:
        memory_pointer: The pointer to the memory buffer.
        memory_length: The length of the memory buffer.
        value: The string to write.
        value_offset: The offset to start writing to.
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
    current_value = read_bytes(
        memory_pointer,
        memory_length,
    )

    new_value = (ctypes.c_ubyte * value_length).from_buffer(value)
    current_value[value_offset : value_offset + value_length] = new_value

    current_value_buffer = (ctypes.c_ubyte * memory_length).from_buffer(current_value)
    ctypes.memmove(memory_pointer, current_value_buffer, memory_length)
