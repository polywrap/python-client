from typing import Dict, Optional
from polywrap_client import PolywrapClient
from polywrap_core import Any, ClientConfig, Uri
from polywrap_plugin import PluginModule, PluginPackage
import pytest
from polywrap_uri_resolvers import (
    MaybeUriOrManifest,
    PackageResolver,
    RecursiveResolver,
    UriResolverAggregator,
    ExtendableUriResolver,
)


class MockPluginExtensionResolver(PluginModule[None]):
    URI = Uri.from_str("wrap://package/test-resolver")

    def __init__(self):
        super().__init__(None)

    def tryResolveUri(
        self, args: Dict[str, Any], *_: Any
    ) -> Optional[MaybeUriOrManifest]:
        if args.get("authority") != "test":
            return None

        match args.get("path"):
            case "from":
                return {"uri": Uri.from_str("test/to").uri}
            case "package":
                return {"manifest": bytes()}
            case "error":
                raise ValueError("test error")
            case _:
                return None


