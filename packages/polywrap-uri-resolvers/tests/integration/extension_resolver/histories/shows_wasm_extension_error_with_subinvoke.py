EXPECTED = [
    'wrap://test/error => UriResolverAggregator => error (SubInvocation exception encountered\ncode: 51 WRAPPER INVOKE ABORTED\nuri: wrap://package/subinvoke-resolver\nmethod: tryResolveUri\nargs: {\n  "authority": "test",\n  "path": "error"\n} \nsource: { file: "src/wrap/module/wrapped.rs", row: 35, col: 21 }\n\nAnother exception was encountered during execution:\nWrapError: __wrap_abort: Test error\ncode: 51 WRAPPER INVOKE ABORTED\nuri: wrap://package/test-resolver\nmethod: tryResolveUri\nargs: {\n  "authority": "test",\n  "path": "error"\n} \nsource: { file: "src/wrap/module/wrapped.rs", row: 35, col: 21 })',
    [
        "wrap://test/error => StaticResolver - Miss",
        'wrap://test/error => ExtendableUriResolver => error (SubInvocation exception encountered\ncode: 51 WRAPPER INVOKE ABORTED\nuri: wrap://package/subinvoke-resolver\nmethod: tryResolveUri\nargs: {\n  "authority": "test",\n  "path": "error"\n} \nsource: { file: "src/wrap/module/wrapped.rs", row: 35, col: 21 }\n\nAnother exception was encountered during execution:\nWrapError: __wrap_abort: Test error\ncode: 51 WRAPPER INVOKE ABORTED\nuri: wrap://package/test-resolver\nmethod: tryResolveUri\nargs: {\n  "authority": "test",\n  "path": "error"\n} \nsource: { file: "src/wrap/module/wrapped.rs", row: 35, col: 21 })',
        [
            'wrap://test/error => ResolverExtension (wrap://package/subinvoke-resolver) => error (SubInvocation exception encountered\ncode: 51 WRAPPER INVOKE ABORTED\nuri: wrap://package/subinvoke-resolver\nmethod: tryResolveUri\nargs: {\n  "authority": "test",\n  "path": "error"\n} \nsource: { file: "src/wrap/module/wrapped.rs", row: 35, col: 21 }\n\nAnother exception was encountered during execution:\nWrapError: __wrap_abort: Test error\ncode: 51 WRAPPER INVOKE ABORTED\nuri: wrap://package/test-resolver\nmethod: tryResolveUri\nargs: {\n  "authority": "test",\n  "path": "error"\n} \nsource: { file: "src/wrap/module/wrapped.rs", row: 35, col: 21 })',
            [
                "wrap://package/subinvoke-resolver => Client.loadWrapper => wrapper (wrap://package/subinvoke-resolver)",
                [
                    "wrap://package/subinvoke-resolver => UriResolverAggregator => package (wrap://package/subinvoke-resolver)",
                    [
                        "wrap://package/subinvoke-resolver => StaticResolver - Package (wrap://package/subinvoke-resolver) => package (wrap://package/subinvoke-resolver)"
                    ],
                ],
                'wrap://package/subinvoke-resolver => Client.invokeWrapper => error (SubInvocation exception encountered\ncode: 51 WRAPPER INVOKE ABORTED\nuri: wrap://package/subinvoke-resolver\nmethod: tryResolveUri\nargs: {\n  "authority": "test",\n  "path": "error"\n} \nsource: { file: "src/wrap/module/wrapped.rs", row: 35, col: 21 }\n\nAnother exception was encountered during execution:\nWrapError: __wrap_abort: Test error\ncode: 51 WRAPPER INVOKE ABORTED\nuri: wrap://package/test-resolver\nmethod: tryResolveUri\nargs: {\n  "authority": "test",\n  "path": "error"\n} \nsource: { file: "src/wrap/module/wrapped.rs", row: 35, col: 21 })',
                [
                    "wrap://package/test-resolver => Client.loadWrapper => wrapper (wrap://package/test-resolver)",
                    [
                        "wrap://package/test-resolver => UriResolverAggregator => package (wrap://package/test-resolver)",
                        [
                            "wrap://package/test-resolver => StaticResolver - Package (wrap://package/test-resolver) => package (wrap://package/test-resolver)"
                        ],
                    ],
                    'wrap://package/test-resolver => Client.invokeWrapper => error (__wrap_abort: Test error\ncode: 51 WRAPPER INVOKE ABORTED\nuri: wrap://package/test-resolver\nmethod: tryResolveUri\nargs: {\n  "authority": "test",\n  "path": "error"\n} \nsource: { file: "src/wrap/module/wrapped.rs", row: 35, col: 21 })',
                ],
            ],
        ],
    ],
]
