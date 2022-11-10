from typing import List, Union

from polywrap_core import Uri, UriPackage, UriWrapper

UriResolverLike = Union[Uri, UriPackage, UriWrapper, List["UriResolverLike"]]