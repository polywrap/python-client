from typing import cast

from polywrap_core import Uri, InvokerClient
from polywrap_manifest import AnyWrapManifest

from polywrap_plugin import PluginWrapper, PluginModule
import pytest


def test_plugin_wrapper_invoke(
    greeting_module: PluginModule[None], client: InvokerClient
):
    manifest = cast(AnyWrapManifest, {})

    wrapper = PluginWrapper(greeting_module, manifest)
    args = {"name": "Joe"}

    result = wrapper.invoke(
        uri=Uri.from_str("ens/greeting.eth"),
        method="greeting",
        args=args,
        client=client,
    )
    assert result, "Greetings from: Joe"


def test_plugin_wrapper_get_file(
    greeting_module: PluginModule[None], client: InvokerClient
):
    manifest = cast(AnyWrapManifest, {})

    wrapper = PluginWrapper(greeting_module, manifest)

    with pytest.raises(NotImplementedError):
        wrapper.get_file(
            path="greeting.txt",
            encoding="utf-8",
        )


def test_plugin_wrapper_manifest(
    greeting_module: PluginModule[None], client: InvokerClient
):
    manifest = cast(AnyWrapManifest, {})

    wrapper = PluginWrapper(greeting_module, manifest)

    assert wrapper.manifest is manifest
