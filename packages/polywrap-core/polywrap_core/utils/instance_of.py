"""This module contains the instance_of utility function."""
import inspect
from typing import Any


def instance_of(obj: Any, cls: Any):
    """Check if an object is an instance of a class or any of its parent classes.

    Args:
        obj (Any): any object instance
        cls (Any): class to check against

    Returns:
        bool: True if obj is an instance of cls or any of its parent classes, False otherwise
    """
    return cls in inspect.getmro(obj.__class__)
