EXPECTED = [
    'wrap://test/error => UriResolverAggregator => error (Test error\ncode: 51 WRAPPER INVOKE ABORTED\nuri: wrap://package/test-resolver\nmethod: tryResolveUri\nargs: {\n  "authority": "test",\n  "path": "error"\n} )',
    [
        "wrap://test/error => StaticResolver - Miss",
        'wrap://test/error => ExtendableUriResolver => error (Test error\ncode: 51 WRAPPER INVOKE ABORTED\nuri: wrap://package/test-resolver\nmethod: tryResolveUri\nargs: {\n  "authority": "test",\n  "path": "error"\n} )',
        [
            'wrap://test/error => ResolverExtension (wrap://package/test-resolver) => error (Test error\ncode: 51 WRAPPER INVOKE ABORTED\nuri: wrap://package/test-resolver\nmethod: tryResolveUri\nargs: {\n  "authority": "test",\n  "path": "error"\n} )',
            [
                "wrap://package/test-resolver => Client.loadWrapper => wrapper (wrap://package/test-resolver)",
                [
                    "wrap://package/test-resolver => UriResolverAggregator => package (wrap://package/test-resolver)",
                    [
                        "wrap://package/test-resolver => StaticResolver - Package (wrap://package/test-resolver) => package (wrap://package/test-resolver)"
                    ],
                ],
                'wrap://package/test-resolver => Client.invokeWrapper => error (Test error\ncode: 51 WRAPPER INVOKE ABORTED\nuri: wrap://package/test-resolver\nmethod: tryResolveUri\nargs: {\n  "authority": "test",\n  "path": "error"\n} )',
            ],
        ],
    ],
]
