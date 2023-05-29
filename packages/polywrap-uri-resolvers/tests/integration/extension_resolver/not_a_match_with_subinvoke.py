EXPECTED = [
    "wrap://test/not-a-match => UriResolverAggregator",
    [
        "wrap://test/not-a-match => StaticResolver - Miss",
        "wrap://test/not-a-match => ExtendableUriResolver",
        [
            "wrap://test/not-a-match => ResolverExtension (wrap://package/subinvoke-resolver)",
            [
                "wrap://package/subinvoke-resolver => Client.loadWrapper => wrapper (wrap://package/subinvoke-resolver)",
                [
                    "wrap://package/subinvoke-resolver => UriResolverAggregator => package (wrap://package/subinvoke-resolver)",
                    [
                        "wrap://package/subinvoke-resolver => StaticResolver - Package (wrap://package/subinvoke-resolver) => package (wrap://package/subinvoke-resolver)"
                    ],
                ],
                "wrap://package/subinvoke-resolver => Client.invokeWrapper",
                [
                    "wrap://package/test-resolver => Client.loadWrapper => wrapper (wrap://package/test-resolver)",
                    [
                        "wrap://package/test-resolver => UriResolverAggregator => package (wrap://package/test-resolver)",
                        [
                            "wrap://package/test-resolver => StaticResolver - Package (wrap://package/test-resolver) => package (wrap://package/test-resolver)"
                        ],
                    ],
                    "wrap://package/test-resolver => Client.invokeWrapper",
                ],
            ],
        ],
    ],
]
