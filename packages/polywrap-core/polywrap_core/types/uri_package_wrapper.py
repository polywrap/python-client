from typing import Union

from .uri import Uri
from .uri_package import UriPackage
from .uri_wrapper import UriWrapper

UriPackageOrWrapper = Union[Uri, UriWrapper, UriPackage]
