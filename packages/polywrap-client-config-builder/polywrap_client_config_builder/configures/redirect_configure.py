"""This module contains the redirect configure class for the client config builder."""
from typing import Dict, List, Union, cast

from polywrap_core import Uri

from ..types import BuilderConfig, ClientConfigBuilder


class RedirectConfigure:
    """Allows configuring the URI redirects."""

    config: BuilderConfig

    def get_redirect(self, uri: Uri) -> Union[Uri, None]:
        """Return the redirect for the given uri."""
        return self.config.redirects.get(uri)

    def get_redirects(self) -> Dict[Uri, Uri]:
        """Return the redirects from the builder's config."""
        return self.config.redirects

    def set_redirect(self, from_uri: Uri, to_uri: Uri) -> ClientConfigBuilder:
        """Set the redirect from a URI to another URI in the builder's config,\
            overiding any existing values."""
        self.config.redirects[from_uri] = to_uri
        return cast(ClientConfigBuilder, self)

    def set_redirects(self, uri_redirects: Dict[Uri, Uri]) -> ClientConfigBuilder:
        """Set the redirects in the builder's config, overiding any existing values."""
        self.config.redirects.update(uri_redirects)
        return cast(ClientConfigBuilder, self)

    def remove_redirect(self, uri: Uri) -> ClientConfigBuilder:
        """Remove the redirect for the given uri."""
        self.config.redirects.pop(uri, None)
        return cast(ClientConfigBuilder, self)

    def remove_redirects(self, uris: List[Uri]) -> ClientConfigBuilder:
        """Remove the redirects for the given uris."""
        for uri in uris:
            self.remove_redirect(uri)
        return cast(ClientConfigBuilder, self)
