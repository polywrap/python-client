"""This module contains the UriRedirect type."""
from dataclasses import dataclass

from polywrap_core import Uri


@dataclass(slots=True, kw_only=True)
class UriRedirect:
    """UriRedirect is a type that represents a redirect from one uri to another.

    Attributes:
        from_uri (Uri): The uri to redirect from.
        to_uri (Uri): The uri to redirect to.
    """

    from_uri: Uri
    to_uri: Uri
