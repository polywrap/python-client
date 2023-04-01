# import asyncio
# from typing import Any, Dict

# from pathlib import Path
# from polywrap_core import Invoker, Uri, InvokerOptions, UriWrapper, Wrapper
# from polywrap_plugin import PluginModule, PluginWrapper
# from polywrap_uri_resolvers import StaticResolver
# from polywrap_manifest import AnyWrapManifest
# from polywrap_result import Result, Ok, Err
# from polywrap_client import PolywrapClient, PolywrapClientConfig
# from pytest import fixture


# @fixture
# def timer_module():
#     class TimerModule(PluginModule[None, str]):
#         def __init__(self, config: None):
#             super().__init__(config)

#         async def sleep(self, args: Dict[str, Any], client: Invoker):
#             await asyncio.sleep(args["time"])
#             print(f"Woke up after {args['time']} seconds")
#             return Ok(True)

#     return TimerModule(None)

# @fixture
# def simple_wrap_manifest():
#     wrap_path = Path(__file__).parent / "cases" / "simple-invoke" / "wrap.info"
#     with open(wrap_path, "rb") as f:
#         yield f.read()

# @fixture
# def timer_wrapper(timer_module: PluginModule[None, str], simple_wrap_manifest: AnyWrapManifest):
#     return PluginWrapper(module=timer_module, manifest=simple_wrap_manifest)


# async def test_timer(timer_wrapper: Wrapper):
#     uri_wrapper = UriWrapper(uri=Uri("ens/timer.eth"), wrapper=timer_wrapper)
#     resolver = StaticResolver.from_list([uri_wrapper]).unwrap()

#     config = PolywrapClientConfig(resolver=resolver)

#     client = PolywrapClient(config)
#     uri = Uri('ens/timer.eth') or Uri(f'fs/{Path(__file__).parent.joinpath("cases", "big-number").absolute()}')
#     args = { "time": 1 }
#     options = InvokerOptions(uri=uri, method="sleep", args=args, encode_result=False)
#     result = await client.invoke(options)
#     assert result.unwrap() == True
