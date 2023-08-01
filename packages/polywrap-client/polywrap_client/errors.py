"""This module contains the errors raised by the Polywrap client."""

import json
from textwrap import dedent

from polywrap_core import Uri, UriResolutionContext, WrapError, build_clean_uri_history


class WrapNotFoundError(WrapError):
    """Raised when a wrap is not found."""

    uri: Uri
    resolution_context: UriResolutionContext

    def __init__(self, uri: Uri, resolution_context: UriResolutionContext):
        """Initialize a new WrapNotFoundError instance."""
        self.uri = uri
        self.resolution_context = resolution_context

        uri_history = build_clean_uri_history(resolution_context.get_history())
        super().__init__(
            dedent(
                f"""
                Error resolving URI "{uri.uri}"
                URI not found
                Resolution Stack: {
                    json.dumps(uri_history, indent=2)
                }
                """
            )
        )
