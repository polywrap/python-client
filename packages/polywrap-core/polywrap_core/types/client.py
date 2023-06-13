"""This module contains the Client interface."""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Protocol, Union

from polywrap_manifest import AnyWrapManifest, DeserializeManifestOptions

from .invoker_client import InvokerClient
from .uri import Uri
from .uri_resolver import UriResolver


class Client(InvokerClient, Protocol):
    """Client protocol defines core set of functionalities\
        for interacting with a wrapper."""

    def get_interfaces(self) -> Dict[Uri, List[Uri]]:
        """Get dictionary of interfaces and their implementations.

        Returns:
            Dict[Uri, List[Uri]]: Dictionary of interfaces and their implementations where\
                key is interface URI and value is list of implementation uris.
        """
        ...

    def get_envs(self) -> Dict[Uri, Any]:
        """Get dictionary of environments.

        Returns:
            Dict[Uri, Any]: Dictionary of environments where key is URI and value is env.
        """
        ...

    def get_env_by_uri(self, uri: Uri) -> Union[Any, None]:
        """Get environment by URI.

        Args:
            uri (Uri): URI of the Wrapper.

        Returns:
            Union[Any, None]: env if found, otherwise None.
        """
        ...

    def get_uri_resolver(self) -> UriResolver:
        """Get URI resolver.

        Returns:
            UriResolver: URI resolver.
        """
        ...

    def get_file(
        self, uri: Uri, path: str, encoding: Optional[str] = "utf-8"
    ) -> Union[bytes, str]:
        """Get file from URI.

        Args:
            uri (Uri): URI of the wrapper.
            path (str): Path to the file.
            encoding (Optional[str]): Encoding of the file.

        Returns:
            Union[bytes, str]]: file contents.
        """
        ...

    def get_manifest(
        self, uri: Uri, options: Optional[DeserializeManifestOptions] = None
    ) -> AnyWrapManifest:
        """Get manifest from URI.

        Args:
            uri (Uri): URI of the wrapper.
            options (Optional[DeserializeManifestOptions]): \
                Options for getting manifest from the wrapper.

        Returns:
            AnyWrapManifest: Manifest of the wrapper.
        """
        ...


__all__ = ["Client"]
