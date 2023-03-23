"""This module contains GetFileOptions type."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True, kw_only=True)
class GetFileOptions:
    """Options for getting a file from a wrapper.

    Attributes:
        path (str): Path to the file.
        encoding (Optional[str]): Encoding of the file.
    """

    path: str
    encoding: Optional[str] = "utf-8"
