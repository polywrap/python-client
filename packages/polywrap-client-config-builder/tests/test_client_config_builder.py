# """
# Polywrap Python Client.

# The Test suite for the Polywrap Client Config Builder uses pytest to
# test the various methods of the ClientConfigBuilder class. These tests
# include sample code for configuring the client's:
# - Envs
# - Interfaces
# - Packages
# - Redirects
# - Wrappers
# - Resolvers

# docs.polywrap.io
# Copyright 2022 Polywrap
# """

# from abc import ABC
# from dataclasses import asdict
# from typing import Any, Dict, Generic, List, Optional, TypeVar, Union, cast

# from polywrap_client import PolywrapClient
# from polywrap_core import (
#     AnyWrapManifest,
#     GetFileOptions,
#     GetManifestOptions,
#     InvocableResult,
#     InvokeOptions,
#     Invoker,
#     IUriResolver,
#     IWrapPackage,
#     Uri,
#     UriPackage,
#     UriWrapper,
#     Wrapper,
# )
# from polywrap_result import Err, Ok, Result

# from polywrap_client_config_builder import (
#     BaseClientConfigBuilder,
#     ClientConfig,
#     ClientConfigBuilder,
# )

# UriResolverLike = Union[Uri, UriPackage, UriWrapper, List["UriResolverLike"]]


# # Mocked Classes for the tests (class fixtures arent supported in pytest)
# pw = PolywrapClient()
# resolver: IUriResolver = pw.get_uri_resolver()
# TConfig = TypeVar('TConfig')
# TResult = TypeVar('TResult')

# class MockedModule(Generic[TConfig, TResult], ABC):
#     env: Dict[str, Any]
#     config: TConfig

#     def __init__(self, config: TConfig):
#         self.config = config

#     def set_env(self, env: Dict[str, Any]) -> None:
#         self.env = env

#     async def __wrap_invoke__(self, method: str, args: Dict[str, Any], client: Invoker) -> Result[TResult]:
#         methods: List[str] = [name for name in dir(self) if name == method]

#         if not methods:
#             return Err.from_str(f"{method} is not defined in plugin")

#         callable_method = getattr(self, method)
#         return Ok(callable_method(args, client)) if callable(callable_method) else Err.from_str(f"{method} is an attribute, not a method")


# class MockedWrapper(Wrapper, Generic[TConfig, TResult]):
#     module: MockedModule[TConfig, TResult]

#     def __init__(self, module: MockedModule[TConfig, TResult], manifest: AnyWrapManifest) -> None:
#         self.module = module
#         self.manifest = manifest

#     async def invoke(
#         self, options: InvokeOptions, invoker: Invoker
#     ) -> Result[InvocableResult]:
#         env = options.env or {}
#         self.module.set_env(env)

#         args: Union[Dict[str, Any], bytes] = options.args or {}
#         decoded_args: Dict[str, Any] = msgpack_decode(args) if isinstance(args, bytes) else args

#         result: Result[TResult] = await self.module.__wrap_invoke__(options.method, decoded_args, invoker)

#         if result.is_err():
#             return cast(Err, result.err)

#         return Ok(InvocableResult(result=result,encoded=False))


#     async def get_file(self, options: GetFileOptions) -> Result[Union[str, bytes]]:
#         return Err.from_str("client.get_file(..) is not implemented for plugins")

#     def get_manifest(self) -> Result[AnyWrapManifest]:
#         return Ok(self.manifest)

# class MockedPackage(Generic[TConfig, TResult], IWrapPackage):
#     module: MockedModule[TConfig, TResult]
#     manifest: AnyWrapManifest

#     def __init__(
#         self, 
#         module: MockedModule[TConfig, TResult],
#         manifest: AnyWrapManifest
#     ):
#         self.module = module
#         self.manifest = manifest

#     async def create_wrapper(self) -> Result[Wrapper]:
#         return Ok(MockedWrapper(module=self.module, manifest=self.manifest))

#     async def get_manifest(self, options: Optional[GetManifestOptions] = None) -> Result[AnyWrapManifest]:
#         return Ok(self.manifest)



# def test_client_config_structure_starts_empty():
#     ccb = ClientConfigBuilder()
#     client_config = ccb.build()
#     result = ClientConfig(
#         envs={},
#         interfaces={}, 
#         resolver = [],
#         wrappers = [],
#         packages=[],
#         redirects={}
#         )
#     assert asdict(client_config) == asdict(result)


# def test_client_config_structure_sets_env():
#     ccb = ClientConfigBuilder()
#     uri = Uri("wrap://ens/eth.plugin.one"), 
#     env = { 'color': "red", 'size': "small" }
#     ccb = ccb.set_env(
#         uri = uri, 
#         env = env
#         )
#     client_config = ccb.build()
#     assert asdict(client_config) == asdict(ClientConfig(envs={uri: env}, interfaces={}, resolver = [], wrappers=[], packages=[], redirects={}))


# # ENVS 

# def test_client_config_builder_set_env(env_varA, env_uriX):
#     ccb = ClientConfigBuilder()
#     envs = { env_uriX: env_varA }
#     ccb = ccb.set_env( env_varA, env_uriX)
#     client_config = ccb.build()
#     assert asdict(client_config) == asdict(ClientConfig(envs=envs, interfaces={}, resolver = [], wrappers=[], packages=[], redirects={}))

# def test_client_config_builder_add_env(env_varA, env_uriX):
#     ccb = ClientConfigBuilder() # instantiate new client config builder
#     ccb = ccb.add_env(env = env_varA, uri = env_uriX) # add env to client config builder    
#     client_config: ClientConfig = ccb.build() # build a client config object
#     print(client_config)
#     assert asdict(client_config) == asdict(ClientConfig(envs={env_uriX: env_varA}, interfaces={}, resolver = [], wrappers=[], packages=[], redirects={}))

# def test_client_config_builder_add_env_updates_env_value(env_varA,env_varB, env_uriX):
#     ccb = ClientConfigBuilder() # instantiate new client config builder
#     ccb = ccb.add_env(env = env_varA, uri = env_uriX) # add env to client config builder
#     client_config: ClientConfig = ccb.build() # build a client config object
#     assert asdict(client_config) == asdict(ClientConfig(envs={env_uriX: env_varA}, interfaces={}, resolver = [], wrappers=[], packages=[], redirects={}))
#     ccb = ccb.add_env(env = env_varB, uri = env_uriX) # update value of env var on client config builder
#     client_config: ClientConfig = ccb.build() # build a new client config object
#     assert asdict(client_config) == asdict(ClientConfig(envs={env_uriX: env_varB}, interfaces={}, resolver = [], wrappers=[], packages=[], redirects={}))

# def test_client_config_builder_set_env_and_add_env_updates_and_add_values(env_varA, env_varB, env_varN, env_varM, env_varS, env_uriX, env_uriY):
#     ccb = ClientConfigBuilder()
#     ccb = ccb.set_env(env_varA, env_uriX) # set the environment variables A
#     client_config: ClientConfig = ccb.build()
#     assert asdict(client_config) == asdict(ClientConfig(envs={env_uriX: env_varA}, interfaces={}, resolver = [], wrappers=[], packages=[], redirects={}))

#     ccb = ccb.set_env(env_varB, env_uriX) # set new vars on the same Uri
#     client_config: ClientConfig = ccb.build()
#     assert asdict(client_config) == asdict(ClientConfig(envs={env_uriX: env_varB}, interfaces={}, resolver = [], wrappers=[], packages=[], redirects={}))

#     ccb = ccb.add_env(env_varM, env_uriY) # add new env vars on a new Uri
#     client_config: ClientConfig = ccb.build()
#     assert asdict(client_config) == asdict(ClientConfig(
#         envs={
#             env_uriX: env_varB,
#             env_uriY: env_varM
#         }, 
#         interfaces={}, resolver = [], wrappers=[], packages=[], redirects={}))

#     # add new env vars on the second Uri, while also updating the Env vars of dog and season
#     ccb = ccb.add_envs([env_varN, env_varS], env_uriY)
#     new_envs = {**env_varM, **env_varN, **env_varS}
#     print(new_envs)
#     client_config = ccb.build()
#     assert asdict(client_config) == asdict(ClientConfig(envs = {env_uriX: env_varB, env_uriY: new_envs}, interfaces={}, resolver = [], wrappers=[], packages=[], redirects={}))

# # INTERFACES AND IMPLEMENTATIONS

# def test_client_config_builder_adds_interface_implementations():
#     ccb = ClientConfigBuilder()
#     interfaces_uri = Uri("wrap://ens/eth.plugin.one")
#     implementations_uris = [Uri("wrap://ens/eth.plugin.one"), Uri("wrap://ens/eth.plugin.two")]
#     ccb = ccb.add_interface_implementations(interfaces_uri, implementations_uris)
#     client_config = ccb.build()
#     assert asdict(client_config) == asdict(ClientConfig(envs={}, interfaces={interfaces_uri: implementations_uris}, resolver = [], wrappers=[], packages=[], redirects={}))

# # PACKAGES

# def test_client_config_builder_set_package():
#     # wrap_package = IWrapPackage()
#     ccb = ClientConfigBuilder()
#     uri_package = UriPackage(uri=Uri("wrap://ens/eth.plugin.one"),package="Todo")
#     ccb = ccb.set_package(uri_package)
#     client_config = ccb.build()
#     assert asdict(client_config) == asdict(ClientConfig(envs={}, interfaces={}, resolver = [], wrappers=[], packages=[uri_package], redirects={}))


# def test_client_config_builder_set_package():
#     ccb = ClientConfigBuilder()
#     module: MockedModule[None, str] = MockedModule(config=None)
#     manifest = cast(AnyWrapManifest, {})
#      # This implementation below is correct, but the test fails because the UriPackage 
#     # gets instantiated twice and two different instances are created. 
#     # uri_package: UriPackage = UriPackage(uri=env_uriX, package=MockedPackage(module, manifest))
#     # so instead we use the following implementation
#     uri_package = UriPackage(uri=Uri("wrap://ens/eth.plugin.one"),package="Todo")
#     ccb = ccb.set_package(uri_package)
#     client_config = ccb.build()
#     assert asdict(client_config) == asdict(ClientConfig(envs={}, 
#         interfaces={}, resolver = [], wrappers=[], packages=[uri_package], redirects={}))

# def test_client_config_builder_add_package():
#     ccb = ClientConfigBuilder()
#     uri_package = UriPackage(uri=Uri("wrap://ens/eth.plugin.one"),package="Todo")
#     ccb = ccb.add_package(uri_package)
#     client_config = ccb.build()
#     assert asdict(client_config) == asdict(ClientConfig(envs={}, interfaces={}, 
#         resolver = [], wrappers=[], packages=[uri_package], redirects={}))

# def test_client_config_builder_add_package_updates_packages_list():
#     ccb = ClientConfigBuilder()
#     uri_package1 = UriPackage(uri=Uri("wrap://ens/eth.plugin.one"),package="Todo")
#     ccb = ccb.add_package(uri_package1)
#     client_config = ccb.build()
#     assert asdict(client_config) == asdict(ClientConfig(envs={}, interfaces={},
#         resolver = [], wrappers=[], packages=[uri_package1], redirects={}))
#     uri_package2 = UriPackage(uri=Uri("wrap://ens/eth.plugin.one"),package="Updated")
#     ccb = ccb.add_package(uri_package2)
#     client_config = ccb.build()
#     assert asdict(client_config) == asdict(ClientConfig(envs={}, interfaces={}, 
#         resolver = [], wrappers=[], packages=[uri_package1, uri_package2], redirects={}))

# def test_client_config_builder_add_multiple_packages():
#     ccb = ClientConfigBuilder()
#     uri_package1 = UriPackage(uri=Uri("wrap://ens/eth.plugin.one"),package="Todo")
#     uri_package2 = UriPackage(uri=Uri("wrap://ens/eth.plugin.one"),package="Updated")
#     ccb = ccb.add_packages([uri_package1, uri_package2])
#     client_config = ccb.build()
#     assert asdict(client_config) == asdict(ClientConfig(envs={}, interfaces={}, resolver = [],
#         wrappers=[], packages=[uri_package1, uri_package2], redirects={}))

# def test_client_config_builder_add_packages_removes_packages():
#     ccb = ClientConfigBuilder()
#     uri_package1 = UriPackage(uri=Uri("wrap://ens/eth.plugin.one"),package="Todo")
#     uri_package2 = UriPackage(uri=Uri("wrap://ens/eth.plugin.one"),package="Updated")
#     ccb = ccb.add_packages([uri_package1, uri_package2])
#     client_config = ccb.build()
#     assert asdict(client_config) == asdict(ClientConfig(envs={}, interfaces={}, resolver = [],
#          wrappers=[], packages=[uri_package1, uri_package2], redirects={}))
#     ccb = ccb.remove_package(uri_package1)
#     client_config = ccb.build()
#     assert asdict(client_config) == asdict(ClientConfig(envs={}, interfaces={}, resolver = [],
#         wrappers=[], packages=[uri_package2], redirects={}))

# # WRAPPERS AND PLUGINS

# def test_client_config_builder_add_wrapper1():
#     ccb = ClientConfigBuilder()
#     uri_wrapper = UriWrapper(uri=Uri("wrap://ens/eth.plugin.one"),wrapper="todo")
#     ccb = ccb.add_wrapper(uri_wrapper)
#     client_config = ccb.build()
#     assert asdict(client_config) == asdict(ClientConfig(envs={}, interfaces={}, resolver = [], wrappers=[uri_wrapper], packages=[], redirects={}))
#     # add second wrapper
#     uri_wrapper2 = UriWrapper(uri=Uri("wrap://ens/eth.plugin.two"),wrapper="Todo")    
#     ccb = ccb.add_wrapper(uri_wrapper2)
#     client_config = ccb.build()
#     assert asdict(client_config) == asdict(ClientConfig(envs={}, interfaces={}, resolver = [], wrappers=[uri_wrapper, uri_wrapper2], packages=[], redirects={}))


# def test_client_config_builder_add_wrapper2():
#     ccb = ClientConfigBuilder()
#     wrapper = Uri("wrap://ens/uni.wrapper.eth")
#     ccb = ccb.add_wrapper(wrapper)
#     client_config = ccb.build()
#     assert asdict(client_config) == asdict(ClientConfig(envs={}, interfaces={}, resolver = [], wrappers=[wrapper], packages=[], redirects={}))

# def test_client_config_builder_adds_multiple_wrappers():
#     ccb = ClientConfigBuilder()
#     wrappers = [Uri("wrap://ens/uni.wrapper.eth"), Uri("wrap://ens/https.plugin.eth")]
#     ccb = ccb.add_wrappers(wrappers)
#     client_config = ccb.build()
#     assert asdict(client_config) == asdict(ClientConfig(envs={}, interfaces={}, resolver = [], wrappers=wrappers, packages=[], redirects={}))

# def test_client_config_builder_removes_wrapper():
#     ccb = ClientConfigBuilder()
#     wrapper = Uri("wrap://ens/uni.wrapper.eth")
#     ccb = ccb.add_wrapper(wrapper)
#     client_config = ccb.build()
#     assert asdict(client_config) == asdict(ClientConfig(envs={}, interfaces={}, resolver = [], wrappers=[wrapper], packages=[], redirects={}))
#     ccb = ccb.remove_wrapper(wrapper)
#     client_config = ccb.build()
#     assert asdict(client_config) == asdict(ClientConfig(envs={}, interfaces={}, resolver = [], wrappers=[], packages=[], redirects={}))

# # RESOLVER 

# def test_client_config_builder_set_uri_resolver():
#     ccb = ClientConfigBuilder()
#     resolver: UriResolverLike = Uri("wrap://ens/eth.resolver.one")
#     ccb = ccb.set_resolver(resolver)
#     client_config = ccb.build()
#     assert asdict(client_config) == asdict(ClientConfig(envs={}, interfaces={}, resolver=[resolver], wrappers=[], packages=[], redirects={}))
    
# def test_client_config_builder_add_resolver():
#     # set a first resolver
#     ccb = ClientConfigBuilder()
#     resolverA = Uri("wrap://ens/eth.resolver.one")
#     ccb: BaseClientConfigBuilder = ccb.set_resolver(resolverA)
#     client_config: ClientConfig = ccb.build()
#     assert asdict(client_config) == asdict(ClientConfig(envs={}, interfaces={}, resolver=[resolverA], wrappers=[], packages=[], redirects={}))
    
#     # add a second resolver
#     resolverB = Uri("wrap://ens/eth.resolver.two")
#     ccb = ccb.add_resolver(resolverB)
#     client_config: ClientConfig = ccb.build()
#     assert asdict(client_config) == asdict(ClientConfig(envs={}, interfaces={}, resolver=[resolverA, resolverB], wrappers=[], packages=[], redirects={}))

#     # add a third and fourth resolver
#     resolverC = Uri("wrap://ens/eth.resolver.three")
#     resolverD = Uri("wrap://ens/eth.resolver.four")
#     ccb = ccb.add_resolvers([resolverC, resolverD])
#     client_config: ClientConfig = ccb.build()
#     resolvers: List[UriResolverLike] = [resolverA, resolverB, resolverC, resolverD]
#     assert asdict(client_config) == asdict(ClientConfig(envs={}, interfaces={}, resolver=resolvers, wrappers=[], packages=[], redirects={}))

# # REDIRECTS

# def test_client_config_builder_sets_uri_redirects(env_uriX, env_uriY, env_uriZ):
#     # set a first redirect
#     ccb = ClientConfigBuilder()
#     ccb = ccb.set_uri_redirect(env_uriX, env_uriY)
#     client_config: ClientConfig = ccb.build()
#     assert asdict(client_config) == asdict(ClientConfig(envs={}, interfaces={}, resolver=[], wrappers=[], packages=[],
#         redirects={env_uriX: env_uriY}))
    
#     # add a second redirect
#     ccb = ccb.set_uri_redirect(env_uriY, env_uriZ)
#     client_config: ClientConfig = ccb.build()
#     assert asdict(client_config) == asdict(ClientConfig(envs={}, interfaces={}, resolver=[], wrappers=[], packages=[],
#         redirects={env_uriX: env_uriY, env_uriY: env_uriZ}))

#     # update the first redirect
#     ccb.set_uri_redirect(env_uriX, env_uriZ)
#     client_config: ClientConfig = ccb.build()
#     assert asdict(client_config) == asdict(ClientConfig(envs={}, interfaces={}, resolver=[], wrappers=[], packages=[],
#          redirects={env_uriX: env_uriZ, env_uriY: env_uriZ}))

# def test_client_config_builder_removes_uri_redirects(env_uriX, env_uriY, env_uriZ):
#     ccb = ClientConfigBuilder()
#     ccb = ccb.set_uri_redirect(env_uriX, env_uriY)
#     ccb = ccb.set_uri_redirect(env_uriY, env_uriZ)
#     client_config: ClientConfig = ccb.build()
#     assert asdict(client_config) == asdict(ClientConfig(envs={}, interfaces={}, resolver=[], wrappers=[], packages=[],
#         redirects={env_uriX: env_uriY, env_uriY: env_uriZ}))
    
#     ccb = ccb.remove_uri_redirect(env_uriX)
#     client_config: ClientConfig = ccb.build()
#     assert asdict(client_config) == asdict(ClientConfig(envs={}, interfaces={}, resolver=[], wrappers=[], packages=[],
#         redirects={env_uriY: env_uriZ}))



# def test_client_config_builder_sets_many_uri_redirects(env_uriX,env_uriY, env_uriZ):

#     # set a first redirect
#     ccb = ClientConfigBuilder()
#     ccb = ccb.set_uri_redirects([{
#             env_uriX: env_uriY,
#         }] )
#     client_config: ClientConfig = ccb.build()
#     assert asdict(client_config) == asdict(ClientConfig(envs={}, interfaces={}, resolver=[], wrappers=[], packages=[], redirects={env_uriX: env_uriY}))

#     # updates that first redirect to a new value
#     ccb = ccb.set_uri_redirects([{
#             env_uriX: env_uriZ,
#         }] )
#     client_config: ClientConfig = ccb.build()
#     assert asdict(client_config) == asdict(ClientConfig(envs={}, interfaces={}, resolver=[], wrappers=[], packages=[], redirects={env_uriX: env_uriZ}))

#     # add a second redirect
#     ccb = ccb.set_uri_redirects([{
#             env_uriY: env_uriX,
#         }] )
#     client_config: ClientConfig = ccb.build()
#     assert asdict(client_config) == asdict(ClientConfig(envs={}, interfaces={}, resolver=[], wrappers=[], packages=[], redirects={env_uriX: env_uriZ, env_uriY: env_uriX}))

#     # add a third redirect and update the first redirect
#     ccb = ccb.set_uri_redirects([{
#             env_uriX: env_uriY,
#             env_uriZ: env_uriY,
#         }] )
#     client_config: ClientConfig = ccb.build()
#     assert asdict(client_config) == asdict(ClientConfig(envs={}, interfaces={}, resolver=[], wrappers=[], packages=[],
#         redirects={
#         env_uriX: env_uriY, 
#         env_uriY: env_uriX, 
#         env_uriZ: env_uriY
#         }))


# # GENERIC ADD FUNCTION

# def test_client_config_builder_generic_add(env_varA,env_uriX, env_uriY):
#     # Test adding package, wrapper, resolver, interface, and env with the ccb.add method
#     ccb = ClientConfigBuilder()
    
#     # starts empty
#     client_config = ccb.build()
#     assert asdict(client_config) == asdict(ClientConfig(envs={}, interfaces={},
#         resolver = [], wrappers=[], packages=[], redirects={}))

#     # add an env
#     new_config = ClientConfig(envs={env_uriX: env_varA}, interfaces={}, resolver = [], wrappers=[], packages=[], redirects={})
#     ccb = ccb.add(new_config)
#     client_config1 = ccb.build()
#     assert asdict(client_config1) == asdict(new_config)

#     # add a resolver
#     new_resolvers = ClientConfig(resolver=[Uri("wrap://ens/eth.resolver.one")], envs={}, interfaces={}, wrappers=[], packages=[], redirects={})
#     ccb = ccb.add(new_resolvers)
#     client_config2 = ccb.build()
#     assert asdict(client_config2) == asdict(ClientConfig(envs={env_uriX: env_varA}, interfaces={},
#         resolver = [Uri("wrap://ens/eth.resolver.one")], wrappers=[], packages=[], redirects={}))

#     # add a second resolver
#     new_resolver = ClientConfig(resolver=[Uri("wrap://ens/eth.resolver.two")], envs={}, interfaces={}, wrappers=[], packages=[], redirects={})
#     ccb = ccb.add(new_resolver)
#     client_config5 = ccb.build()
#     assert asdict(client_config5) == asdict(ClientConfig(envs={env_uriX: env_varA}, interfaces={},
#         resolver = [Uri("wrap://ens/eth.resolver.one"), Uri("wrap://ens/eth.resolver.two")], wrappers=[], packages=[], redirects={}))


#     # add a wrapper
#     new_wrapper = ClientConfig(wrappers=[Uri("wrap://ens/uni.wrapper.eth")], envs={}, interfaces={}, resolver = [], packages=[], redirects={})
#     ccb = ccb.add(new_wrapper)
#     client_config3 = ccb.build()
#     assert asdict(client_config3) == asdict(ClientConfig(envs={env_uriX: env_varA}, interfaces={},
#         resolver = [Uri("wrap://ens/eth.resolver.one"), Uri("wrap://ens/eth.resolver.two")],
#         wrappers=[Uri("wrap://ens/uni.wrapper.eth")], packages=[], redirects={}))

#     # add an interface
#     interfaces: Dict[Uri, List[Uri]] = {Uri("wrap://ens/eth.interface.eth"): [env_uriX,env_uriY]}
#     new_interface = ClientConfig(interfaces=interfaces, envs={}, resolver = [], wrappers=[], packages=[], redirects={})
#     ccb = ccb.add(new_interface)
#     client_config4 = ccb.build()
#     assert asdict(client_config4) == asdict(ClientConfig(envs={env_uriX: env_varA}, interfaces=interfaces,
#         resolver = [Uri("wrap://ens/eth.resolver.one"), Uri("wrap://ens/eth.resolver.two")],
#         wrappers=[Uri("wrap://ens/uni.wrapper.eth")], packages=[], redirects={}))

#     # add a package
#     uri_package = UriPackage(uri=Uri("wrap://ens/eth.plugin.one"),package="Todo")
#     new_package = ClientConfig(packages=[uri_package], envs={}, interfaces={}, resolver = [], wrappers=[], redirects={})
#     ccb = ccb.add(new_package)
#     client_config6 = ccb.build()
#     assert asdict(client_config6) == asdict(ClientConfig(envs={env_uriX: env_varA}, interfaces=interfaces,
#         resolver = [Uri("wrap://ens/eth.resolver.one"), Uri("wrap://ens/eth.resolver.two")],
#         wrappers=[Uri("wrap://ens/uni.wrapper.eth")], packages=[uri_package], redirects={}))


