"""
This type stub file was generated by pyright.
"""

from polywrap_core import Uri
from .abc.resolver_with_history import IResolverWithHistory

class RedirectResolver(IResolverWithHistory):
    __slots__ = ...
    from_uri: Uri
    to_uri: Uri
    def __init__(self, from_uri: Uri, to_uri: Uri) -> None:
        ...
    
    def get_step_description(self) -> str:
        ...
    


