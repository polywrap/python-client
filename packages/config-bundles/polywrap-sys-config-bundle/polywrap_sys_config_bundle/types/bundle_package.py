"""This module contains the type for the bundle package."""
from dataclasses import dataclass
from typing import Any, Optional

from polywrap_client_config_builder import ClientConfigBuilder
from polywrap_core import Uri, WrapPackage


@dataclass(slots=True, kw_only=True)
class BundlePackage:
    """A bundle item is a single item in a bundle."""

    uri: Uri
    package: Optional[WrapPackage] = None
    implements: Optional[list[Uri]] = None
    redirects_from: Optional[list[Uri]] = None
    env: Optional[Any] = None

    def add_to_builder(self, builder: ClientConfigBuilder) -> None:
        """Add the bundle item to the client config builder."""
        if self.package:
            builder.set_package(self.uri, self.package)
        if self.implements:
            for interface in self.implements:
                builder.add_interface_implementations(interface, [self.uri])
        if self.redirects_from:
            for redirect in self.redirects_from:
                builder.set_redirect(redirect, self.uri)
        if self.env:
            builder.set_env(self.uri, self.env)


__all__ = ["BundlePackage"]
