from dataclasses import dataclass

from polywrap_core import Uri, Wrapper


@dataclass(slots=True, kw_only=True)
class UriWrapper:
    uri: Uri
    wrapper: Wrapper
