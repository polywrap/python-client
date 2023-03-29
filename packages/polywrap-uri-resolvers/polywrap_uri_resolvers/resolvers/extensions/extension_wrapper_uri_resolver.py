from typing import Optional, TypedDict, cast
from polywrap_core import (
    Client,
    InvokerClient,
    IUriResolutionContext,
    UriWrapper,
    UriPackage,
    Uri,
    TryResolveUriOptions,
    UriPackageOrWrapper,
    InvokeOptions,
    Wrapper,
)
from polywrap_msgpack import msgpack_decode

from polywrap_wasm import WasmPackage

from .uri_resolver_extension_file_reader import UriResolverExtensionFileReader
from ..abc import ResolverWithHistory
from ...errors import UriResolverExtensionError, UriResolverExtensionNotFoundError
from ...utils import get_env_from_uri_history


class MaybeUriOrManifest(TypedDict):
    uri: Optional[str]
    manifest: Optional[bytes]


class ExtensionWrapperUriResolver(ResolverWithHistory):
    __slots__ = "extension_wrapper_uri"

    extension_wrapper_uri: Uri

    def __init__(self, extension_wrapper_uri: Uri):
        self.extension_wrapper_uri = extension_wrapper_uri

    def get_step_description(self) -> str:
        return f"ResolverExtension ({self.extension_wrapper_uri})"

    async def _try_resolve_uri(
        self,
        uri: Uri,
        client: InvokerClient[UriPackageOrWrapper],
        resolution_context: IUriResolutionContext[UriPackageOrWrapper],
    ) -> UriPackageOrWrapper:
        sub_context = resolution_context.create_sub_context()

        try:
            extension_wrapper = await self._load_resolver_extension(client, sub_context)
            uri_or_manifest = await self._try_resolve_uri_with_extension(
                uri, extension_wrapper, client, sub_context
            )

            if uri_or_manifest.get("uri"):
                return Uri.from_str(cast(str, uri_or_manifest["uri"]))

            if uri_or_manifest.get("manifest"):
                package = WasmPackage(
                    UriResolverExtensionFileReader(
                        self.extension_wrapper_uri, uri, client
                    ),
                    uri_or_manifest["manifest"],
                )
                return UriPackage(uri, package)

            return uri

        except Exception as err:
            raise UriResolverExtensionError(
                f"Failed to resolve uri: {uri}, using extension resolver: ({self.extension_wrapper_uri})"
            ) from err

    async def _load_resolver_extension(
        self,
        client: InvokerClient[UriPackageOrWrapper],
        resolution_context: IUriResolutionContext[UriPackageOrWrapper],
    ) -> Wrapper[UriPackageOrWrapper]:
        result = await client.try_resolve_uri(
            TryResolveUriOptions(
                uri=self.extension_wrapper_uri, resolution_context=resolution_context
            )
        )

        extension_wrapper: Wrapper[UriPackageOrWrapper]

        if isinstance(result, UriPackage):
            extension_wrapper = await cast(
                UriPackage[UriPackageOrWrapper], result
            ).package.create_wrapper()
        elif isinstance(result, UriWrapper):
            extension_wrapper = cast(UriWrapper[UriPackageOrWrapper], result).wrapper
        else:
            raise UriResolverExtensionNotFoundError(
                self.extension_wrapper_uri, resolution_context.get_history()
            )
        return extension_wrapper

    async def _try_resolve_uri_with_extension(
        self,
        uri: Uri,
        extension_wrapper: Wrapper[UriPackageOrWrapper],
        client: InvokerClient[UriPackageOrWrapper],
        resolution_context: IUriResolutionContext[UriPackageOrWrapper],
    ) -> MaybeUriOrManifest:
        env = (
            get_env_from_uri_history(
                resolution_context.get_resolution_path(), cast(Client, client)
            )
            if hasattr(client, "get_env_by_uri")
            else None
        )

        result = await extension_wrapper.invoke(
            InvokeOptions(
                uri=self.extension_wrapper_uri,
                method="tryResolveUri",
                args={
                    "authority": uri.authority,
                    "path": uri.path,
                },
                env=env,
            ),
            client,
        )

        return msgpack_decode(result) if isinstance(result, bytes) else result
