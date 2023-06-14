"""This module defines the ResolutionContextOverrideClient class."""
from typing import Any, List, Optional

from polywrap_core import InvokerClient, Uri, UriResolutionContext


class ResolutionContextOverrideClient(InvokerClient):
    """A client that overrides the resolution context of the wrapped client.

    Args:
        client (InvokerClient): The wrapped client.
        resolution_context (Optional[UriResolutionContext]): \
            The resolution context to use.
    """

    client: InvokerClient
    resolution_context: Optional[UriResolutionContext]

    __slots__ = ("client", "resolution_context")

    def __init__(
        self, client: InvokerClient, resolution_context: Optional[UriResolutionContext]
    ):
        """Initialize a new ResolutionContextOverrideClient instance."""
        self.client = client
        self.resolution_context = resolution_context

    def invoke(
        self,
        uri: Uri,
        method: str,
        args: Optional[Any] = None,
        env: Optional[Any] = None,
        resolution_context: Optional[UriResolutionContext] = None,
        encode_result: Optional[bool] = False,
    ) -> Any:
        """Invoke the Wrapper based on the provided InvokerOptions.

        Args:
            uri (Uri): Uri of the wrapper
            method (str): Method to be executed
            args (Optional[Any]) : Arguments for the method, structured as a dictionary
            env (Optional[Any]): Override the client's config for all invokes within this invoke.
            resolution_context (Optional[UriResolutionContext]): A URI resolution context
            encode_result (Optional[bool]): If True, the result will be encoded

        Returns:
            Any: invocation result.

        Raises:
            WrapInvocationError: If the plugin method is not defined\
                or is not callable.
            WrapAbortError: If the plugin method raises an exception.
            MsgpackDecodeError: If the plugin method returns invalid msgpack.
        """
        return self.client.invoke(
            uri,
            method,
            args,
            env,
            self.resolution_context,
            encode_result,
        )

    def get_implementations(
        self, uri: Uri, apply_resolution: bool = True
    ) -> Optional[List[Uri]]:
        """Get implementations of an interface with its URI.

        Args:
            uri (Uri): URI of the interface.
            apply_resolution (bool): If True, apply resolution to the URI and interfaces.

        Returns:
            Optional[List[Uri]]: List of implementations or None if not found.
        """
        return self.client.get_implementations(uri, apply_resolution)

    def try_resolve_uri(
        self, uri: Uri, resolution_context: UriResolutionContext | None = None
    ) -> Any:
        """Try to resolve a URI to a wrap package, a wrapper, or a URI.

        Args:
            uri (Uri): The URI to resolve.
            resolution_context (UriResolutionContext): The resolution context.

        Returns:
            Any: URI Resolution Result.
        """
        return self.client.try_resolve_uri(uri, self.resolution_context)
