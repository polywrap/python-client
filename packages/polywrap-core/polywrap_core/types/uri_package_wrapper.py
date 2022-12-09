from __future__ import annotations

from typing import Union

from .uri import Uri
from .wrap_package import IWrapPackage
from .wrapper import Wrapper

UriPackageOrWrapper = Union[Uri, Wrapper, IWrapPackage]
