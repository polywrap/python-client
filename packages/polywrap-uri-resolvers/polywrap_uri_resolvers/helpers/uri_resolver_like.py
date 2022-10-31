from typing import List, Union

from polywrap_core import Uri, IUriResolver, UriPackage, UriWrapper

UriResolverLike = Union[Uri, IUriResolver, UriPackage, UriWrapper, List["UriResolverLike"]]