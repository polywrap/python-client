"""This module contains the interface configure class for the client config builder."""
from abc import ABC
from typing import Dict, List, Union

from polywrap_core import Uri

from ..types import BuilderConfig, ClientConfigBuilder


class InterfaceConfigure(ClientConfigBuilder, ABC):
    """Allows configuring the interface-implementations."""

    config: BuilderConfig

    def get_interfaces(self) -> Dict[Uri, List[Uri]]:
        """Return all registered interface and its implementations\
            from the builder's config."""
        return self.config.interfaces

    def get_interface_implementations(self, uri: Uri) -> Union[List[Uri], None]:
        """Return the interface for the given uri."""
        return self.config.interfaces.get(uri)

    def add_interface_implementations(
        self, interface_uri: Uri, implementations_uris: List[Uri]
    ) -> ClientConfigBuilder:
        """Add a list of implementation URIs for the given interface URI to the builder's config."""
        if interface_uri in self.config.interfaces.keys():
            existing_implementations = set(self.config.interfaces[interface_uri])
            for implementation_uri in implementations_uris:
                if implementation_uri not in existing_implementations:
                    self.config.interfaces[interface_uri].append(implementation_uri)
        else:
            self.config.interfaces[interface_uri] = implementations_uris
        return self

    def remove_interface_implementations(
        self, interface_uri: Uri, implementations_uris: List[Uri]
    ) -> ClientConfigBuilder:
        """Remove the implementations for the given interface uri."""
        self.config.interfaces[interface_uri] = [
            uri
            for uri in self.config.interfaces[interface_uri]
            if uri not in implementations_uris
        ]
        return self

    def remove_interface(self, interface_uri: Uri) -> ClientConfigBuilder:
        """Remove the interface for the given uri."""
        self.config.interfaces.pop(interface_uri, None)
        return self
