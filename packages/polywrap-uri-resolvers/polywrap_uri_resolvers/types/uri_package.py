from dataclasses import dataclass

from polywrap_core import IWrapPackage, Uri


@dataclass(slots=True, kw_only=True)
class UriPackage:
    uri: Uri
    package: IWrapPackage
