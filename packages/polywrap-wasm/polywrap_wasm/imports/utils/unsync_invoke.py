"""This module contains the unsync_invoke function."""
from typing import Any

from polywrap_core import Invoker, InvokerOptions, UriPackageOrWrapper
from unsync import Unfuture, unsync


@unsync
async def unsync_invoke(
    invoker: Invoker[UriPackageOrWrapper], options: InvokerOptions[UriPackageOrWrapper]
) -> Unfuture[Any]:
    """Perform an unsync invoke call."""
    return await invoker.invoke(options)
