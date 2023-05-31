# from pathlib import Path

# from polywrap_client_config_builder import PolywrapClientConfigBuilder
# from polywrap_plugin import PluginPackage
# from polywrap_client import PolywrapClient
# from polywrap_manifest import deserialize_wrap_manifest
# from polywrap_core import (
#     Uri,
#     FileReader,
#     ClientConfig,
# )
# from polywrap_uri_resolvers import (
#     BaseUriResolver,
#     FsUriResolver,
#     SimpleFileReader,
#     StaticResolver,
# )
# from polywrap_wasm import WasmWrapper


# def test_invoke(
#     client: PolywrapClient,
#     simple_file_reader: FileReader,
#     simple_wrap_module: bytes,
#     simple_wrap_manifest: bytes,
# ):
#     uri = Uri.from_str(
#         f'fs/{Path(__file__).parent.joinpath("cases", "simple-invoke").absolute()}'
#     )
#     args = {"arg": "hello polywrap"}
#     result = client.invoke(uri=uri, method="simpleMethod", args=args, encode_result=False)

#     assert result == args["arg"]

#     manifest = deserialize_wrap_manifest(simple_wrap_manifest)

#     wrapper = WasmWrapper(
#         file_reader=simple_file_reader,
#         wasm_module=simple_wrap_module,
#         manifest=manifest,
#     )
#     resolver = StaticResolver({Uri.from_str("ens/wrapper.eth"): wrapper})

#     config = ClientConfig(resolver=resolver)
#     client = PolywrapClient(config=config)

#     args = {"arg": "hello polywrap"}
#     result =  client.invoke(        uri=Uri.from_str("ens/wrapper.eth"),
#         method="simpleMethod",
#         args=args,
#         encode_result=False,)

#     assert result == args["arg"]


# def test_subinvoke():
#     uri_resolver = BaseUriResolver(
#         file_reader=SimpleFileReader(),
#         redirects={
#             Uri.from_str("ens/add.eth"): Uri.from_str(
#                 f'fs/{Path(__file__).parent.joinpath("cases", "simple-subinvoke", "subinvoke").absolute()}'
#             ),
#         },
#     )

#     client = PolywrapClient(config=ClientConfig(resolver=uri_resolver))
#     uri = Uri.from_str(
#         f'fs/{Path(__file__).parent.joinpath("cases", "simple-subinvoke", "invoke").absolute()}'
#     )
#     args = {"a": 1, "b": 2}
#     result = client.invoke(uri=uri, method="add", args=args, encode_result=False)

#     assert result == "1 + 2 = 3"


# async def test_interface_implementation():
#     uri_resolver = BaseUriResolver(
#         file_reader=SimpleFileReader(),
#         redirects={},
#     )

#     interface_uri = Uri.from_str("ens/interface.eth")
#     impl_uri = Uri.from_str(
#         f'fs/{Path(__file__).parent.joinpath("cases", "simple-interface", "implementation").absolute()}'
#     )

#     client = PolywrapClient(
#         config=ClientConfig(
#             resolver=uri_resolver, interfaces={interface_uri: [impl_uri]}
#         )
#     )
#     uri = Uri.from_str(
#         f'fs/{Path(__file__).parent.joinpath("cases", "simple-interface", "wrapper").absolute()}'
#     )
#     args = {"arg": {"str": "hello", "uint8": 2}}
#     result = client.invoke(uri=uri, method="moduleMethod", args=args, encode_result=False)
#     assert client.get_implementations(interface_uri) == [impl_uri]
#     assert result == {"str": "hello", "uint8": 2}


# def test_get_env_by_uri():
#     uri_resolver = BaseUriResolver(
#         file_reader=SimpleFileReader(),
#         redirects={},
#     )
#     uri = Uri.from_str(
#         f'fs/{Path(__file__).parent.joinpath("cases", "simple-env").absolute()}'
#     )
#     env = {"externalArray": [1, 2, 3], "externalString": "hello"}

#     client = PolywrapClient(
#         config=ClientConfig(
#             envs={uri: env},
#             resolver=uri_resolver,
#         )
#     )
#     assert client.get_env_by_uri(uri) == env


# async def test_env():
#     uri_resolver = BaseUriResolver(
#         file_reader=SimpleFileReader(),
#         redirects={},
#     )

#     uri = Uri.from_str(
#         f'fs/{Path(__file__).parent.joinpath("cases", "simple-env").absolute()}'
#     )
#     env = {"externalArray": [1, 2, 3], "externalString": "hello"}

#     client = PolywrapClient(
#         config=ClientConfig(
#             envs={uri: env},
#             resolver=uri_resolver,
#         )
#     )

#     result = client.invoke(        uri=uri,
#         method="externalEnvMethod",
#         args={},
#         encode_result=False,)

#     assert result == env


# async def test_complex_subinvocation(adder_plugin: PluginPackage[None]):
#     config = (
#         PolywrapClientConfigBuilder()
#         .add_resolver(FsUriResolver(SimpleFileReader()))
#         .set_redirect(
#             Uri.from_str("ens/imported-subinvoke.eth"),
#             Uri.from_str(
#                 f'fs/{Path(__file__).parent.joinpath("cases", "subinvoke", "00-subinvoke").absolute()}'
#             ),
#         )
#         .set_redirect(
#             Uri.from_str("ens/imported-invoke.eth"),
#             Uri.from_str(
#                 f'fs/{Path(__file__).parent.joinpath("cases", "subinvoke", "01-invoke").absolute()}'
#             ),
#         )
#         .set_package(
#             Uri.from_str("plugin/adder"),
#             adder_plugin,
#         )
#     ).build()

#     client = PolywrapClient(config)
#     uri = Uri.from_str(
#         f'fs/{Path(__file__).parent.joinpath("cases", "subinvoke", "02-consumer").absolute()}'
#     )
#     args = {"a": 1, "b": 1}
#     result = client.invoke(uri=uri, method="addFromPluginAndIncrement", args=args)

#     assert result == 4
