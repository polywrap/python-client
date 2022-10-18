from typing import Any

from ..types import Wrapper


async def init_wrapper(package_or_wrapper: Any) -> Wrapper:
    if hasattr(package_or_wrapper, "create_wrapper"):
        return await package_or_wrapper.createWrapper()
    return package_or_wrapper
