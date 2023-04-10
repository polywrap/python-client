"""This module contains the package configure class for the client config builder."""
from typing import Dict, List, Union

from polywrap_core import Uri, UriPackageOrWrapper, WrapPackage

from ..types import ClientConfigBuilder


class PackageConfigure(ClientConfigBuilder):
    """Allows configuring the WRAP packages."""

    def get_package(self, uri: Uri) -> Union[WrapPackage[UriPackageOrWrapper], None]:
        """Return the package for the given uri."""
        return self.config.packages.get(uri)

    def get_packages(self) -> Dict[Uri, WrapPackage[UriPackageOrWrapper]]:
        """Return the packages from the builder's config."""
        return self.config.packages

    def set_package(
        self, uri: Uri, package: WrapPackage[UriPackageOrWrapper]
    ) -> ClientConfigBuilder:
        """Set the package by uri in the builder's config, overiding any existing values."""
        self.config.packages[uri] = package
        return self

    def set_packages(
        self, uri_packages: Dict[Uri, WrapPackage[UriPackageOrWrapper]]
    ) -> ClientConfigBuilder:
        """Set the packages in the builder's config, overiding any existing values."""
        self.config.packages.update(uri_packages)
        return self

    def remove_package(self, uri: Uri) -> ClientConfigBuilder:
        """Remove the package for the given uri."""
        self.config.packages.pop(uri, None)
        return self

    def remove_packages(self, uris: List[Uri]) -> ClientConfigBuilder:
        """Remove the packages for the given uris."""
        for uri in uris:
            self.remove_package(uri)
        return self
