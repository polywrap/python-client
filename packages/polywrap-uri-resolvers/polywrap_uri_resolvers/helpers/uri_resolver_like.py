from typing import List, Union

from polywrap_core import IUriResolver, UriPackage, UriWrapper

UriResolverLike = Union[IUriResolver, UriPackage, UriWrapper, List["UriResolverLike"]]