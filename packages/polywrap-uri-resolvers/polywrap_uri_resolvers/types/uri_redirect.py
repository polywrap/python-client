from dataclasses import dataclass

from polywrap_core import Uri


@dataclass(slots=True, kw_only=True)
class UriRedirect:
    from_uri: Uri
    to_uri: Uri
