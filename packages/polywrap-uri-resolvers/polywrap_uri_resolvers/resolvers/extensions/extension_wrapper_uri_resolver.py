"""This module contains the ExtensionWrapperUriResolver class."""
from typing import Optional, TypedDict, cast

from polywrap_core import (
    Client,
    InvokeOptions,
    InvokerClient,
    IUriResolutionContext,
    TryResolveUriOptions,
    Uri,
    UriPackage,
    UriPackageOrWrapper,
    UriWrapper,
    Wrapper,
)
from polywrap_msgpack import msgpack_decode
from polywrap_wasm import WasmPackage

from ...errors import UriResolverExtensionError, UriResolverExtensionNotFoundError
from ...utils import get_env_from_uri_history
from ..abc import ResolverWithHistory
from .uri_resolver_extension_file_reader import UriResolverExtensionFileReader


class MaybeUriOrManifest(TypedDict):
    """Defines a type for the return value of the extension wrapper's\
        tryResolveUri function.

    The extension wrapper's tryResolveUri function can return either a uri\
        or a manifest. This type defines the return value of the function.
    """

    uri: Optional[str]
    manifest: Optional[bytes]


class ExtensionWrapperUriResolver(ResolverWithHistory):
    """Defines a resolver that resolves a uri to a wrapper by using an extension wrapper.

    This resolver resolves a uri to a wrapper by using an extension wrapper.\
        The extension wrapper is resolved using the extension wrapper uri resolver.\
        The extension wrapper is then used to resolve the uri to a wrapper.

    Attributes:
        extension_wrapper_uri (Uri): The uri of the extension wrapper.
    """

    __slots__ = ("extension_wrapper_uri",)

    extension_wrapper_uri: Uri

    def __init__(self, extension_wrapper_uri: Uri):
        """Initialize a new ExtensionWrapperUriResolver instance.

        Args:
            extension_wrapper_uri (Uri): The uri of the extension wrapper.
        """
        self.extension_wrapper_uri = extension_wrapper_uri

    def get_step_description(self) -> str:
        """Get the description of the resolver step.

        Returns:
            str: The description of the resolver step.
        """
        return f"ResolverExtension ({self.extension_wrapper_uri})"

    async def _try_resolve_uri(
        self,
        uri: Uri,
        client: InvokerClient[UriPackageOrWrapper],
        resolution_context: IUriResolutionContext[UriPackageOrWrapper],
    ) -> UriPackageOrWrapper:
        """Try to resolve a URI to a wrap package, a wrapper, or a URI.

        This method tries to resolve the uri using the extension wrapper.\
            If the extension wrapper returns a uri, the uri is returned.\
            If the extension wrapper returns a manifest, the manifest is used\
            to create a wrapper and the wrapper is returned.
        
        Args:
            uri (Uri): The URI to resolve.
            client (InvokerClient[UriPackageOrWrapper]): The client to use for\
                resolving the URI.
            resolution_context (IUriResolutionContext[UriPackageOrWrapper]): The\
                resolution context.
        
        Returns:
            UriPackageOrWrapper: The resolved URI package, wrapper, or URI.
        """
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
                f"Failed to resolve uri: {uri}, using extension resolver: "
                f"({self.extension_wrapper_uri})"
            ) from err

    async def _load_resolver_extension(
        self,
        client: InvokerClient[UriPackageOrWrapper],
        resolution_context: IUriResolutionContext[UriPackageOrWrapper],
    ) -> Wrapper[UriPackageOrWrapper]:
        """Load the URI resolver extension wrapper.

        Args:
            client (InvokerClient[UriPackageOrWrapper]): The client to use for\
                resolving the URI.
            resolution_context (IUriResolutionContext[UriPackageOrWrapper]): The\
                resolution context.
        """
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
        """Try to resolve a URI to a uri or a manifest using the extension wrapper.

        Args:
            uri (Uri): The URI to resolve.
            extension_wrapper (Wrapper[UriPackageOrWrapper]): The extension wrapper.
            client (InvokerClient[UriPackageOrWrapper]): The client to use for\
                resolving the URI.
            resolution_context (IUriResolutionContext[UriPackageOrWrapper]): The\
                resolution context.

        Returns:
            MaybeUriOrManifest: The resolved URI or manifest.
        """
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
