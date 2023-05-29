from typing import Dict, Optional
from polywrap_core import Any, InvokerClient, Uri
from polywrap_plugin import PluginModule, PluginPackage
from polywrap_uri_resolvers import (
    MaybeUriOrManifest,
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


def mock_plugin_extension_resolver():
    return PluginPackage(MockPluginExtensionResolver(), NotImplemented)


class MockSubinvokePluginResolver(PluginModule[None]):
    URI = Uri.from_str("wrap://package/test-subinvoke-resolver")

    def __init__(self):
        super().__init__(None)

    def tryResolveUri(
        self, args: Dict[str, Any], client: InvokerClient, *_: Any
    ) -> Optional[MaybeUriOrManifest]:
        return client.invoke(
            uri=Uri.from_str("package/test-resolver"), method="tryResolveUri", args=args
        )


def mock_subinvoke_plugin_resolver():
    return PluginPackage(MockSubinvokePluginResolver(), NotImplemented)