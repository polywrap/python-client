from __future__ import annotations

from dataclasses import dataclass
from textwrap import dedent
from typing import Any, List, Optional, Union, cast,Dict

from polywrap_core import (
    Client,
    ClientConfig,
    Env,
    GetEnvsOptions,
    GetFileOptions,
    GetManifestOptions,
    GetUriResolversOptions,
    InterfaceImplementations,
    InvokerOptions,
    IUriResolutionContext,
    IUriResolver,
    TryResolveUriOptions,
    Uri,
    UriPackage,
    UriPackageOrWrapper,
    UriResolutionContext,
    Wrapper,
)
from polywrap_manifest import AnyWrapManifest
from polywrap_msgpack import msgpack_decode, msgpack_encode
from polywrap_result import Err, Ok, Result
from polywrap_uri_resolvers import FsUriResolver, SimpleFileReader


@dataclass(slots=True, kw_only=True)
class PolywrapClientConfig(ClientConfig):
    pass


class PolywrapClient(Client):
    _config: PolywrapClientConfig

    def __init__(self, config: Optional[PolywrapClientConfig] = None):
        # TODO: this is naive solution need to use polywrap-client-config-builder once we have it
        self._config = config or PolywrapClientConfig(
            resolver=FsUriResolver(file_reader=SimpleFileReader())
        )

    def get_config(self):
        return self._config

    def get_uri_resolver(
        self, options: Optional[GetUriResolversOptions] = None
    ) -> IUriResolver:
        return self._config.resolver

    def get_envs(self, options: Optional[GetEnvsOptions] = None) -> Union[Dict[Uri, Dict[str, Any]], None]:
        envs = self._config.envs
        return envs

    def get_interfaces(self) -> List[InterfaceImplementations]:
        return self._config.interfaces

    def get_implementations(self, uri: Uri) -> Result[List[Uri]]:
        if interface_implementations := next(
            filter(lambda x: x.interface == uri, self._config.interfaces), None
        ):
            return Ok(interface_implementations.implementations)
        else:
            return Err.from_str(f"Unable to find implementations for uri: {uri}")

    def get_env_by_uri(self, uri: Uri, options: Optional[GetEnvsOptions] = None
    ) -> Union[Env, Dict[Uri, Dict[str, Any]], None]:
        print(f"--> Continue by calling get_env_by_uri: {uri=}") 
        # print("uri=", uri)
        print(type(uri))
        # print("---------")
        # print("uri.uri=", uri.uri)
        # print("type(uri)", type(uri.uri))
        print("---------")
        # print(f"{self.get_envs()=}")
        # print(f"{type(self.get_envs())=}")
        # print(f"{dir(self.get_envs())}")
        # #print(f"{self.get_envs()}")
        # #print(f"{self.get_envs()=}")
        # print("---------")
        # print("options=", options)
        # print(type(options))
        # print("---------")        
        #fn = lambda env: env.uri == uri.uri
        #print(fn(uri))
        envs = self.get_envs()

        # print("---------")
        print(f"{envs=}")
        # if isinstance(envs, dict):
        #     print(type(envs.get(uri)))
        #     return envs.get(uri)
        print("---------") 
        return envs

    async def get_file(
        self, uri: Uri, options: GetFileOptions
    ) -> Result[Union[bytes, str]]:
        loaded_wrapper = (await self.load_wrapper(uri)).unwrap()
        return await loaded_wrapper.get_file(options)

    async def get_manifest(
        self, uri: Uri, options: Optional[GetManifestOptions] = None
    ) -> Result[AnyWrapManifest]:
        loaded_wrapper = (await self.load_wrapper(uri)).unwrap()
        return loaded_wrapper.get_manifest()

    async def try_resolve_uri(
        self, options: TryResolveUriOptions
    ) -> Result[UriPackageOrWrapper]:
        uri = options.uri
        uri_resolver = self._config.resolver
        resolution_context = options.resolution_context or UriResolutionContext()

        return await uri_resolver.try_resolve_uri(uri, self, resolution_context)

    async def load_wrapper(
        self, uri: Uri, resolution_context: Optional[IUriResolutionContext] = None
    ) -> Result[Wrapper]:
        resolution_context = resolution_context or UriResolutionContext()

        result = await self.try_resolve_uri(
            TryResolveUriOptions(uri=uri, resolution_context=resolution_context)
        )
        if result.is_err() == True:
            return cast(Err, result)
        if result.is_ok() == True and result.ok is None:
            # FIXME: add resolution stack
            return Err.from_str(
                dedent(
                    f"""
                    Error resolving URI "{uri.uri}"
                    Resolution Stack: NotImplemented
                    """
                )
            )

        uri_package_or_wrapper = result.unwrap()

        if isinstance(uri_package_or_wrapper, Uri):
            # FIXME: add resolution stack
            return Err.from_str(
                dedent(
                    f"""
                    Error resolving URI "{uri.uri}"
                    URI not found
                    Resolution Stack: NotImplemented
                    """
                )
            )

        if isinstance(uri_package_or_wrapper, UriPackage):
            return await uri_package_or_wrapper.package.create_wrapper()

        return Ok(uri_package_or_wrapper.wrapper)

    async def invoke(self, options: InvokerOptions) -> Result[Any]:
        resolution_context = options.resolution_context or UriResolutionContext()
        wrapper_result = await self.load_wrapper(
            options.uri, resolution_context=resolution_context
        )
        if wrapper_result.is_err():
            return cast(Err, wrapper_result)
        wrapper = wrapper_result.unwrap()

        # print(self.get_env_by_uri(options.uri))
        env = self.get_env_by_uri(options.uri)
        # print(f"{env=}")
        #print(f"{env.env=}")
        # print('options=', options)
        options.env = options.env or (env if env else None)

        result = await wrapper.invoke(options, invoker=self)
        if result.is_err():
            return cast(Err, result)
        invocable_result = result.unwrap()

        if options.encode_result and not invocable_result.encoded:
            encoded = msgpack_encode(invocable_result.result)
            return Ok(encoded)

        if (
            not options.encode_result
            and invocable_result.encoded
            and isinstance(invocable_result.result, (bytes, bytearray))
        ):
            decoded: Any = msgpack_decode(invocable_result.result)
            return Ok(decoded)

        return Ok(invocable_result.result)
