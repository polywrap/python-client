"""This module contains the wrapper configure class for the client config builder."""
from typing import Dict, List, Union

from polywrap_core import Uri, UriPackageOrWrapper, Wrapper

from ..types import ClientConfigBuilder


class WrapperConfigure(ClientConfigBuilder):
    """Allows configuring the wrappers."""

    def get_wrapper(self, uri: Uri) -> Union[Wrapper[UriPackageOrWrapper], None]:
        """Return the set wrapper for the given uri."""
        return self.config.wrappers.get(uri)

    def get_wrappers(self) -> Dict[Uri, Wrapper[UriPackageOrWrapper]]:
        """Return the wrappers from the builder's config."""
        return self.config.wrappers

    def set_wrapper(
        self, uri: Uri, wrapper: Wrapper[UriPackageOrWrapper]
    ) -> ClientConfigBuilder:
        """Set the wrapper by uri in the builder's config, overiding any existing values."""
        self.config.wrappers[uri] = wrapper
        return self

    def set_wrappers(
        self, uri_wrappers: Dict[Uri, Wrapper[UriPackageOrWrapper]]
    ) -> ClientConfigBuilder:
        """Set the wrappers in the builder's config, overiding any existing values."""
        self.config.wrappers.update(uri_wrappers)
        return self

    def remove_wrapper(self, uri: Uri) -> ClientConfigBuilder:
        """Remove the wrapper for the given uri."""
        self.config.wrappers.pop(uri, None)
        return self

    def remove_wrappers(self, uris: List[Uri]) -> ClientConfigBuilder:
        """Remove the wrappers for the given uris."""
        for uri in uris:
            self.remove_wrapper(uri)
        return self
