EXPECTED = [
    'wrap://test/error => UriResolverAggregator => error (__wrap_abort: Test error\ncode: 51 WRAPPER INVOKE ABORTED\nuri: wrap://package/test-resolver\nmethod: tryResolveUri\nargs: {\n  "authority": "test",\n  "path": "error"\n} \nsource: { file: "src/wrap/module/wrapped.rs", row: 35, col: 21 })',
    [
        "wrap://test/error => StaticResolver - Miss",
        'wrap://test/error => ExtendableUriResolver => error (__wrap_abort: Test error\ncode: 51 WRAPPER INVOKE ABORTED\nuri: wrap://package/test-resolver\nmethod: tryResolveUri\nargs: {\n  "authority": "test",\n  "path": "error"\n} \nsource: { file: "src/wrap/module/wrapped.rs", row: 35, col: 21 })',
        [
            'wrap://test/error => ResolverExtension (wrap://package/test-resolver) => error (__wrap_abort: Test error\ncode: 51 WRAPPER INVOKE ABORTED\nuri: wrap://package/test-resolver\nmethod: tryResolveUri\nargs: {\n  "authority": "test",\n  "path": "error"\n} \nsource: { file: "src/wrap/module/wrapped.rs", row: 35, col: 21 })',
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
]
