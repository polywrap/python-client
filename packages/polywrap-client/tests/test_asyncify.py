# # Polywrap Python Client - https://polywrap.io
# # BigNumber wrapper schema - https://wrappers.io/v/ipfs/Qme2YXThmsqtfpiUPHJUEzZSBiqX3woQxxdXbDJZvXrvAD

# from pathlib import Path
# from polywrap_client import PolywrapClient
# from polywrap_core import Uri


# async def test_asyncify(client: PolywrapClient):
#     uri = Uri.from_str(
#         f'fs/{Path(__file__).parent.joinpath("cases", "asyncify").absolute()}'
#     )
#     args = {"numberOfTimes": 40}
#     subsequent_invokes_result = await client.invoke(
#         uri=uri, method="subsequentInvokes", args=args
#     )
#     subsequent_invokes_expected = [str(i) for i in range(40)]

#     assert subsequent_invokes_result == subsequent_invokes_expected

#     local_var_method_result = await client.invoke(
#         uri=uri, method="localVarMethod", args=None
#     )

#     assert local_var_method_result == True

#     global_var_method_result = await client.invoke(
#         uri=uri, method="globalVarMethod", args=None
#     )
#     assert global_var_method_result == True

#     large_str = "polywrap" * 10000
#     set_data_with_large_args_result = await client.invoke(
#         uri=uri, method="setDataWithLargeArgs", args={"value": large_str}
#     )
#     assert set_data_with_large_args_result == large_str

#     large_str = "polywrap" * 10000
#     set_data_with_large_args_result = await client.invoke(
#         uri=uri, method="setDataWithLargeArgs", args={"value": large_str}
#     )
#     assert set_data_with_large_args_result == large_str

#     set_data_with_many_args_args = {
#         "valueA": "polywrap a",
#         "valueB": "polywrap b",
#         "valueC": "polywrap c",
#         "valueD": "polywrap d",
#         "valueE": "polywrap e",
#         "valueF": "polywrap f",
#         "valueG": "polywrap g",
#         "valueH": "polywrap h",
#         "valueI": "polywrap i",
#         "valueJ": "polywrap j",
#         "valueK": "polywrap k",
#         "valueL": "polywrap l",
#     }

#     set_data_with_many_args_result = await client.invoke(
#         uri=uri, method="setDataWithManyArgs", args=set_data_with_many_args_args
#     )

#     set_data_with_many_args_expected = "polywrap apolywrap bpolywrap cpolywrap dpolywrap epolywrap fpolywrap gpolywrap hpolywrap ipolywrap jpolywrap kpolywrap l"
#     assert set_data_with_many_args_result == set_data_with_many_args_expected

#     def create_obj(i: int):
#         return {
#             "propA": f"a-{i}",
#             "propB": f"b-{i}",
#             "propC": f"c-{i}",
#             "propD": f"d-{i}",
#             "propE": f"e-{i}",
#             "propF": f"f-{i}",
#             "propG": f"g-{i}",
#             "propH": f"h-{i}",
#             "propI": f"i-{i}",
#             "propJ": f"j-{i}",
#             "propK": f"k-{i}",
#             "propL": f"l-{i}",
#         }

#     set_data_with_many_structure_args_args = {
#         "valueA": create_obj(1),
#         "valueB": create_obj(2),
#         "valueC": create_obj(3),
#         "valueD": create_obj(4),
#         "valueE": create_obj(5),
#         "valueF": create_obj(6),
#         "valueG": create_obj(7),
#         "valueH": create_obj(8),
#         "valueI": create_obj(9),
#         "valueJ": create_obj(10),
#         "valueK": create_obj(11),
#         "valueL": create_obj(12),
#     }
#     set_data_with_many_structured_args_result = await client.invoke(
#         uri=uri,
#         method="setDataWithManyStructuredArgs",
#         args=set_data_with_many_structure_args_args,
#     )
#     assert set_data_with_many_structured_args_result == True
