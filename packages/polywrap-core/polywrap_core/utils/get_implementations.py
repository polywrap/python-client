"""This module contains the get_implementations utility."""
from typing import Dict, List, Optional, Set

from ..types import InvokerClient, Uri, UriResolutionContext
from ..types.errors import WrapGetImplementationsError


def _get_final_uri(
    uri: Uri,
    client: Optional[InvokerClient] = None,
    resolution_context: Optional[UriResolutionContext] = None,
) -> Uri:
    if client:
        try:
            return client.try_resolve_uri(uri, resolution_context)
        except Exception as e:
            raise WrapGetImplementationsError(uri, "Failed to resolve redirects") from e
    return uri


def get_implementations(
    interface_uri: Uri,
    interfaces: Dict[Uri, List[Uri]],
    client: Optional[InvokerClient] = None,
    resolution_context: Optional[UriResolutionContext] = None,
) -> Optional[List[Uri]]:
    """Get implementations of an interface with its URI.

    Args:
        interface_uri (Uri): URI of the interface.
        interfaces (Dict[Uri, List[Uri]]): Dictionary of interfaces and their implementations.
        client (Optional[InvokerClient]): The client to use for resolving the URI.
        resolution_context (Optional[UriResolutionContext]): The resolution context to use.

    Raises:
        WrapGetImplementationsError: If the URI cannot be resolved.

    Returns:
        Optional[List[Uri]]: List of implementations or None if not found.
    """
    final_interface_uri = _get_final_uri(interface_uri, client, resolution_context)
    final_implementations: Set[Uri] = set()

    for interface in interfaces:
        final_current_interface_uri = _get_final_uri(
            interface, client, resolution_context
        )
        if final_current_interface_uri == final_interface_uri:
            impls: Set[Uri] = set(interfaces.get(interface, []))
            final_implementations = final_implementations.union(impls)

    return list(final_implementations) if final_implementations else None


__all__ = ["get_implementations"]
