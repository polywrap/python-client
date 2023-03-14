"""This module contains the Client interface."""
from __future__ import annotations

from abc import abstractmethod
from typing import Dict, List, Optional, Union

from polywrap_manifest import AnyWrapManifest
from polywrap_result import Result

from .env import Env
from .invoker_client import InvokerClient
from .options.file import GetFileOptions
from .options.manifest import GetManifestOptions
from .uri import Uri
from .uri_resolver import IUriResolver


class Client(InvokerClient):
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
    def get_uri_resolver(self) -> IUriResolver:
        """Get URI resolver.

        Returns:
            IUriResolver: URI resolver.
        """

    @abstractmethod
    async def get_file(
        self, uri: Uri, options: GetFileOptions
    ) -> Result[Union[bytes, str]]:
        """Get file from URI.

        Args:
            uri: URI of the wrapper.
            options: Options for getting file from the wrapper.

        Returns:
            Result[Union[bytes, str]]: Result of file contents or error.
        """

    @abstractmethod
    async def get_manifest(
        self, uri: Uri, options: Optional[GetManifestOptions] = None
    ) -> Result[AnyWrapManifest]:
        """Get manifest from URI.

        Args:
            uri: URI of the wrapper.
            options: Options for getting manifest from the wrapper.

        Returns:
            Result[AnyWrapManifest]: Result of manifest or error.
        """
