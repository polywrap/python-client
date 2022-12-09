from dataclasses import dataclass
from polywrap_core import Uri, IWrapPackage


@dataclass(slots=True, kw_only=True)
class UriPackage:
    uri: Uri
    package: IWrapPackage
