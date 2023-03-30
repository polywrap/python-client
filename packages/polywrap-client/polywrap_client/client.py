from __future__ import annotations

import json
from dataclasses import dataclass
from textwrap import dedent
from typing import Any, Dict, List, Optional, Union, cast

from polywrap_core import (
    Client,
    ClientConfig,
    Env,
    GetFileOptions,
    GetManifestOptions,
    InvokerOptions,
    IUriResolutionContext,
    UriPackage,
    UriResolver,
    UriWrapper,
    TryResolveUriOptions,
    Uri,
    UriPackageOrWrapper,
    Wrapper,
)
from polywrap_manifest import AnyWrapManifest
from polywrap_msgpack import msgpack_decode, msgpack_encode
from polywrap_uri_resolvers import UriResolutionContext, build_clean_uri_history


@dataclass(slots=True, kw_only=True)
class PolywrapClientConfig(ClientConfig):
    pass


class PolywrapClient(Client):
    _config: PolywrapClientConfig

    def __init__(self, config: PolywrapClientConfig):
        self._config = config

    def get_config(self):
        return self._config

    def get_uri_resolver(self) -> UriResolver:
        return self._config.resolver

    def get_envs(self) -> Dict[Uri, Env]:
        envs: Dict[Uri, Env] = self._config.envs
        return envs

    def get_interfaces(self) -> Dict[Uri, List[Uri]]:
        interfaces: Dict[Uri, List[Uri]] = self._config.interfaces
        return interfaces

    def get_implementations(self, uri: Uri) -> Union[List[Uri], None]:
        interfaces: Dict[Uri, List[Uri]] = self.get_interfaces()
        return interfaces.get(uri)

    def get_env_by_uri(self, uri: Uri) -> Union[Env, None]:
        return self._config.envs.get(uri)

    async def get_file(self, uri: Uri, options: GetFileOptions) -> Union[bytes, str]:
        loaded_wrapper = await self.load_wrapper(uri)
        return await loaded_wrapper.get_file(options)

    async def get_manifest(
        self, uri: Uri, options: Optional[GetManifestOptions] = None
    ) -> AnyWrapManifest:
        loaded_wrapper = await self.load_wrapper(uri)
        return loaded_wrapper.get_manifest()

    async def try_resolve_uri(
        self, options: TryResolveUriOptions[UriPackageOrWrapper]
    ) -> UriPackageOrWrapper:
        uri = options.uri
        uri_resolver = self._config.resolver
        resolution_context = options.resolution_context or UriResolutionContext()

        return await uri_resolver.try_resolve_uri(uri, self, resolution_context)

    async def load_wrapper(
        self,
        uri: Uri,
        resolution_context: Optional[IUriResolutionContext[UriPackageOrWrapper]] = None,
    ) -> Wrapper[UriPackageOrWrapper]:
        resolution_context = resolution_context or UriResolutionContext()

        uri_package_or_wrapper = await self.try_resolve_uri(
            TryResolveUriOptions(uri=uri, resolution_context=resolution_context)
        )

        if isinstance(uri_package_or_wrapper, UriPackage):
            return await cast(
                UriPackage[UriPackageOrWrapper], uri_package_or_wrapper
            ).package.create_wrapper()

        if isinstance(uri_package_or_wrapper, UriWrapper):
            return cast(UriWrapper[UriPackageOrWrapper], uri_package_or_wrapper).wrapper

        raise RuntimeError(
            dedent(
                f"""
                Error resolving URI "{uri.uri}"
                URI not found
                Resolution Stack: {json.dumps(build_clean_uri_history(resolution_context.get_history()), indent=2)}
                """
            )
        )


    async def invoke(self, options: InvokerOptions[UriPackageOrWrapper]) -> Any:
        resolution_context = options.resolution_context or UriResolutionContext()
        wrapper = await self.load_wrapper(
            options.uri, resolution_context=resolution_context
        )
        options.env = options.env or self.get_env_by_uri(options.uri)

        invocable_result = await wrapper.invoke(options, invoker=self)

        if options.encode_result and not invocable_result.encoded:
            encoded = msgpack_encode(invocable_result.result)
            return encoded

        if (
            not options.encode_result
            and invocable_result.encoded
            and isinstance(invocable_result.result, (bytes, bytearray))
        ):
            decoded: Any = msgpack_decode(invocable_result.result)
            return decoded

        return invocable_result.result
