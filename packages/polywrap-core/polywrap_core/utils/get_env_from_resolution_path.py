"""This module contains the utility function for getting the env from the URI history."""
from typing import Any, List, Union

from ..types import Client, Uri


def get_env_from_resolution_path(
    uri_history: List[Uri], client: Client
) -> Union[Any, None]:
    """Get environment variable from URI resolution history.

    Args:
        uri_history (List[Uri]): List of URIs from the URI resolution history
        client (Client): Polywrap client instance to use for getting the env by URI

    Returns:
        env if found, None otherwise
    """
    for uri in uri_history:
        if env := client.get_env_by_uri(uri):
            return env
    return None


__all__ = ["get_env_from_resolution_path"]
