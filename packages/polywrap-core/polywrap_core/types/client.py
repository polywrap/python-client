"""This module contains the Client interface."""
from __future__ import annotations

from abc import abstractmethod
from typing import Dict, List, Optional, Union

from polywrap_manifest import AnyWrapManifest

from .env import Env
from .invoker_client import InvokerClient
from .options.file_options import GetFileOptions
from .options.manifest_options import GetManifestOptions
from .uri import Uri
from .uri_package_wrapper import UriPackageOrWrapper
from .uri_resolver import UriResolver


class Client(InvokerClient[UriPackageOrWrapper]):
    """Client interface defines core set of functionalities\
        for interacting with a wrapper."""

    @abstractmethod
    def get_interfaces(self) -> Dict[Uri, List[Uri]]:
        """Get dictionary of interfaces and their implementations.

        Returns:
            Dict[Uri, List[Uri]]: Dictionary of interfaces and their implementations where\
                key is interface URI and value is list of implementation uris.
        """

    @abstractmethod
    def get_envs(self) -> Dict[Uri, Env]:
        """Get dictionary of environments.

        Returns:
            Dict[Uri, Env]: Dictionary of environments where key is URI and value is env.
        """

    @abstractmethod
    def get_env_by_uri(self, uri: Uri) -> Union[Env, None]:
        """Get environment by URI.

        Args:
            uri (Uri): URI of the Wrapper.

        Returns:
            Union[Env, None]: env if found, otherwise None.
        """

    @abstractmethod
    def get_uri_resolver(self) -> UriResolver:
        """Get URI resolver.

        Returns:
            IUriResolver: URI resolver.
        """

    @abstractmethod
    async def get_file(self, uri: Uri, options: GetFileOptions) -> Union[bytes, str]:
        """Get file from URI.

        Args:
            uri (Uri): URI of the wrapper.
            options (GetFileOptions): Options for getting file from the wrapper.

        Returns:
            Union[bytes, str]]: file contents.
        """

    @abstractmethod
    async def get_manifest(
        self, uri: Uri, options: Optional[GetManifestOptions] = None
    ) -> AnyWrapManifest:
        """Get manifest from URI.

        Args:
            uri (Uri): URI of the wrapper.
            options (Optional[GetManifestOptions]): \
                Options for getting manifest from the wrapper.

        Returns:
            AnyWrapManifest: Manifest of the wrapper.
        """
