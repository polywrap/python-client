"""
This type stub file was generated by pyright.
"""

from dataclasses import dataclass
from typing import Any, Optional, Tuple, Union

@dataclass(slots=True, kw_only=True)
class UriConfig:
    """URI configuration."""
    authority: str
    path: str
    uri: str
    ...


class Uri:
    """
    A Polywrap URI.

    Some examples of valid URIs are:
        wrap://ipfs/QmHASH
        wrap://ens/sub.dimain.eth
        wrap://fs/directory/file.txt
        wrap://uns/domain.crypto
    Breaking down the various parts of the URI, as it applies
    to [the URI standard](https://tools.ietf.org/html/rfc3986#section-3):
    **wrap://** - URI Scheme: differentiates Polywrap URIs.
    **ipfs/** - URI Authority: allows the Polywrap URI resolution algorithm to determine
                an authoritative URI resolver.
    **sub.domain.eth** - URI Path: tells the Authority where the API resides.
    """
    def __init__(self, uri: str) -> None:
        ...
    
    def __str__(self) -> str:
        ...
    
    def __repr__(self) -> str:
        ...
    
    def __hash__(self) -> int:
        ...
    
    def __eq__(self, b: object) -> bool:
        ...
    
    def __lt__(self, b: Uri) -> bool:
        ...
    
    @property
    def authority(self) -> str:
        ...
    
    @property
    def path(self) -> str:
        ...
    
    @property
    def uri(self) -> str:
        ...
    
    @staticmethod
    def equals(a: Uri, b: Uri) -> bool:
        ...
    
    @staticmethod
    def is_uri(value: Any) -> bool:
        ...
    
    @staticmethod
    def is_valid_uri(uri: str, parsed: Optional[UriConfig] = ...) -> Tuple[Union[UriConfig, None], bool]:
        ...
    
    @staticmethod
    def parse_uri(uri: str) -> UriConfig:
        ...
    


