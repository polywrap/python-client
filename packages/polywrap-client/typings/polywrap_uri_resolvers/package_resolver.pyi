"""
This type stub file was generated by pyright.
"""

from polywrap_core import IWrapPackage, Uri
from .abc import IResolverWithHistory

class PackageResolver(IResolverWithHistory):
    __slots__ = ...
    uri: Uri
    wrap_package: IWrapPackage
    def __init__(self, uri: Uri, wrap_package: IWrapPackage) -> None:
        ...
    
    def get_step_description(self) -> str:
        ...
    


