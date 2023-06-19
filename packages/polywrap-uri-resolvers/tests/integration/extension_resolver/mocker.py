import os
from typing import Any, Dict, Optional
from polywrap_core import InvokerClient, Uri, UriPackage
from polywrap_plugin import PluginModule, PluginPackage
from polywrap_test_cases import get_path_to_test_wrappers

from polywrap_uri_resolvers import MaybeUriOrManifest
from polywrap_wasm import WasmPackage


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
                return {"manifest": b"test"}
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


def mock_subinvoke_plugin_resolver() -> PluginPackage[None]:
    return PluginPackage(MockSubinvokePluginResolver(), NotImplemented)


def mock_fs_wasm_package_resolver() -> UriPackage:
    wrapper_module_path = os.path.join(
        get_path_to_test_wrappers(), "resolver", "02-fs", "implementations", "as", "wrap.wasm"
    )
    wrapper_manifest_path = os.path.join(
        get_path_to_test_wrappers(), "resolver", "02-fs", "implementations", "as", "wrap.info"
    )
    with open(wrapper_module_path, "rb") as f:
        module = f.read()

    with open(wrapper_manifest_path, "rb") as f:
        manifest = f.read()
    
    package = WasmPackage(NotImplemented, manifest=manifest, wasm_module=module)
    return UriPackage(uri=Uri.from_str("package/test-fs-resolver"),package=package)
