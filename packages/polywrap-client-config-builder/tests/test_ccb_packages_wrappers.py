from typing import List, Any, Dict, Union
from polywrap_core import Env
from polywrap_core import  Uri
from polywrap_core import IUriResolver, UriPackage, UriWrapper, IWrapPackage
from polywrap_client_config_builder import ClientConfigBuilder
import pytest
from pytest import fixture
from polywrap_client_config_builder import ClientConfig
from dataclasses import asdict
from polywrap_client import PolywrapClient


# polywrap plugins
from abc import ABC
from typing import Any, Dict, TypeVar, Generic, List

from polywrap_core import Invoker, InvokeOptions, InvocableResult, GetFileOptions
from polywrap_result import Err, Ok, Result
from typing import Generic, Optional, cast

from polywrap_core import IWrapPackage, Wrapper, GetManifestOptions
from polywrap_manifest import AnyWrapManifest
from polywrap_result import Ok, Result
from polywrap_msgpack import msgpack_decode


TConfig = TypeVar('TConfig')
TResult = TypeVar('TResult')

class MockedModule(Generic[TConfig, TResult], ABC):
    env: Dict[str, Any]
    config: TConfig

    def __init__(self, config: TConfig):
        self.config = config

    def set_env(self, env: Dict[str, Any]) -> None:
        self.env = env

    async def __wrap_invoke__(self, method: str, args: Dict[str, Any], client: Invoker) -> Result[TResult]:
        methods: List[str] = [name for name in dir(self) if name == method]

        if not methods:
            return Err.from_str(f"{method} is not defined in plugin")

        callable_method = getattr(self, method)
        return Ok(callable_method(args, client)) if callable(callable_method) else Err.from_str(f"{method} is an attribute, not a method")


class MockedWrapper(Wrapper, Generic[TConfig, TResult]):
    module: MockedModule[TConfig, TResult]

    def __init__(self, module: MockedModule[TConfig, TResult], manifest: AnyWrapManifest) -> None:
        self.module = module
        self.manifest = manifest

    async def invoke(
        self, options: InvokeOptions, invoker: Invoker
    ) -> Result[InvocableResult]:
        env = options.env or {}
        self.module.set_env(env)

        args: Union[Dict[str, Any], bytes] = options.args or {}
        decoded_args: Dict[str, Any] = msgpack_decode(args) if isinstance(args, bytes) else args

        result: Result[TResult] = await self.module.__wrap_invoke__(options.method, decoded_args, invoker)

        if result.is_err():
            return cast(Err, result.err)

        return Ok(InvocableResult(result=result,encoded=False))


    async def get_file(self, options: GetFileOptions) -> Result[Union[str, bytes]]:
        return Err.from_str("client.get_file(..) is not implemented for plugins")

    def get_manifest(self) -> Result[AnyWrapManifest]:
        return Ok(self.manifest)

class MockedPackage(Generic[TConfig, TResult], IWrapPackage):
    module: MockedModule[TConfig, TResult]
    manifest: AnyWrapManifest

    def __init__(
        self, 
        module: MockedModule[TConfig, TResult],
        manifest: AnyWrapManifest
    ):
        self.module = module
        self.manifest = manifest

    async def create_wrapper(self) -> Result[Wrapper]:
        return Ok(MockedWrapper(module=self.module, manifest=self.manifest))

    async def get_manifest(self, options: Optional[GetManifestOptions] = None) -> Result[AnyWrapManifest]:
        return Ok(self.manifest)


pw = PolywrapClient()
resolver: IUriResolver = pw.get_uri_resolver()

def test_client_config_builder_set_package():
    # wrap_package = IWrapPackage()
    ccb = ClientConfigBuilder()
    uri_package = UriPackage(uri=Uri("wrap://ens/eth.plugin.one"),package="Todo")
    ccb = ccb.set_package(uri_package)
    client_config = ccb.build()
    assert asdict(client_config) == asdict(ClientConfig(envs={}, interfaces={}, resolver = [], wrappers=[], packages=[uri_package], redirects={}))

def test_client_config_builder_add_wrapper():
    ccb = ClientConfigBuilder()
    uri_wrapper = UriWrapper(uri=Uri("wrap://ens/eth.plugin.one"),wrapper="todo")
    ccb = ccb.add_wrapper(uri_wrapper)
    client_config = ccb.build()
    assert asdict(client_config) == asdict(ClientConfig(envs={}, interfaces={}, resolver = [], wrappers=[uri_wrapper], packages=[], redirects={}))
    # add second wrapper
    uri_wrapper2 = UriWrapper(uri=Uri("wrap://ens/eth.plugin.two"),wrapper="Todo")    
    ccb = ccb.add_wrapper(uri_wrapper2)
    client_config = ccb.build()
    assert asdict(client_config) == asdict(ClientConfig(envs={}, interfaces={}, resolver = [], wrappers=[uri_wrapper, uri_wrapper2], packages=[], redirects={}))