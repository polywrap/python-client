"""This module contains the utility for sanitizing and parsing Wrapper URIs."""
from __future__ import annotations

import re
from dataclasses import dataclass
from functools import total_ordering
from typing import Any, List, Optional, Tuple, Union


@dataclass(slots=True, kw_only=True)
class UriConfig:
    """URI configuration.

    Attributes:
        authority: The authority of the URI.
        path: The path of the URI.
        uri: The URI as a string.
    """

    authority: str
    path: str
    uri: str


@total_ordering
class Uri:
    """Defines a wrapper URI.

    Some examples of valid URIs are:
        wrap://ipfs/QmHASH
        wrap://ens/sub.dimain.eth
        wrap://fs/directory/file.txt
        wrap://uns/domain.crypto
    Breaking down the various parts of the URI, as it applies
    to [the URI standard](https://tools.ietf.org/html/rfc3986#section-3):
    **wrap://** - URI Scheme: differentiates Polywrap URIs.
    **ipfs/** - URI Authority: allows the Polywrap URI resolution algorithm \
        to determine an authoritative URI resolver.
    **sub.domain.eth** - URI Path: tells the Authority where the API resides.
    """

    def __init__(self, uri: str):
        """Initialize a new instance of a wrapper URI by parsing the provided URI.

        Args:
            uri: The URI to parse.
        """
        self._config = Uri.parse_uri(uri)

    def __str__(self) -> str:
        """Return the URI as a string."""
        return self._config.uri

    def __repr__(self) -> str:
        """Return the string URI representation."""
        return f"Uri({self._config.uri})"

    def __hash__(self) -> int:
        """Return the hash of the URI."""
        return hash(self._config.uri)

    def __eq__(self, obj: object) -> bool:
        """Return true if the provided object is a Uri and has the same URI."""
        return self.uri == obj.uri if isinstance(obj, Uri) else False

    def __lt__(self, uri: Uri) -> bool:
        """Return true if the provided Uri has a URI that is lexicographically\
            less than this Uri."""
        return self.uri < uri.uri

    @property
    def authority(self) -> str:
        """Return the authority of the URI."""
        return self._config.authority

    @property
    def path(self) -> str:
        """Return the path of the URI."""
        return self._config.path

    @property
    def uri(self) -> str:
        """Return the URI as a string."""
        return self._config.uri

    @staticmethod
    def equals(first: Uri, second: Uri) -> bool:
        """Return true if the provided URIs are equal."""
        return first.uri == second.uri

    @staticmethod
    def is_uri(value: Any) -> bool:
        """Return true if the provided value is a Uri."""
        return hasattr(value, "uri")

    @staticmethod
    def is_valid_uri(
        uri: str, parsed: Optional[UriConfig] = None
    ) -> Tuple[Union[UriConfig, None], bool]:
        """Check if the provided URI is valid and returns the parsed URI if it is."""
        try:
            result = Uri.parse_uri(uri)
            return result, True
        except ValueError:
            return parsed, False

    @staticmethod
    def parse_uri(uri: str) -> UriConfig:
        """Parse the provided URI and returns a UriConfig object.

        Args:
            uri: The URI to parse.

        Returns:
            A UriConfig object.
        """
        if not uri:
            raise ValueError("The provided URI is empty")
        processed = uri
        # Trim preceding '/' characters
        processed = processed.lstrip("/")
        # Check for the w3:// scheme, add if it isn't there
        wrap_scheme_idx = processed.find("wrap://")
        if wrap_scheme_idx == -1:
            processed = f"wrap://{processed}"

        # If the w3:// is not in the beginning, throw an error
        if wrap_scheme_idx > -1 and wrap_scheme_idx != 0:
            raise ValueError(
                "The wrap:// scheme must be at the beginning of the URI string"
            )

        # Extract the authoriy & path
        result: List[str] = re.findall(
            r"(wrap:\/\/([a-z][a-z0-9-_]+)\/(.*))", processed
        )

        # Remove all empty strings
        if result:
            result = list(filter(lambda x: x not in [" ", ""], result[0]))

        if not result or len(result) != 3:
            raise ValueError(
                f"""URI is malformed, here are some examples of valid URIs:\n
                wrap://ipfs/QmHASH\n
                wrap://ens/domain.eth\n
                ens/domain.eth\n\n
                Invalid URI Received: {uri}
                """
            )

        return UriConfig(uri=processed, authority=result[1], path=result[2])
