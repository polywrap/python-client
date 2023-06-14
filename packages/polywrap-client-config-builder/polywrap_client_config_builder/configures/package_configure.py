"""This module contains the package configure class for the client config builder."""
from typing import Dict, List, Union, cast

from polywrap_core import Uri, WrapPackage

from ..types import BuilderConfig, ClientConfigBuilder


class PackageConfigure:
    """Allows configuring the WRAP packages."""

    config: BuilderConfig

    def get_package(self, uri: Uri) -> Union[WrapPackage, None]:
        """Return the package for the given uri."""
        return self.config.packages.get(uri)

    def get_packages(self) -> Dict[Uri, WrapPackage]:
        """Return the packages from the builder's config."""
        return self.config.packages

    def set_package(self, uri: Uri, package: WrapPackage) -> ClientConfigBuilder:
        """Set the package by uri in the builder's config, overiding any existing values."""
        self.config.packages[uri] = package
        return cast(ClientConfigBuilder, self)

    def set_packages(self, uri_packages: Dict[Uri, WrapPackage]) -> ClientConfigBuilder:
        """Set the packages in the builder's config, overiding any existing values."""
        self.config.packages.update(uri_packages)
        return cast(ClientConfigBuilder, self)

    def remove_package(self, uri: Uri) -> ClientConfigBuilder:
        """Remove the package for the given uri."""
        self.config.packages.pop(uri, None)
        return cast(ClientConfigBuilder, self)

    def remove_packages(self, uris: List[Uri]) -> ClientConfigBuilder:
        """Remove the packages for the given uris."""
        for uri in uris:
            self.remove_package(uri)
        return cast(ClientConfigBuilder, self)
