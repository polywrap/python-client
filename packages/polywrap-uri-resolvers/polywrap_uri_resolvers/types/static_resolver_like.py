from typing import Dict, Union

from polywrap_core import Uri, UriPackageOrWrapper, WrapPackage, Wrapper

StaticResolverLike = Union[
    Dict[Uri, Uri],
    Dict[Uri, WrapPackage[UriPackageOrWrapper]],
    Dict[Uri, Wrapper[UriPackageOrWrapper]],
]
