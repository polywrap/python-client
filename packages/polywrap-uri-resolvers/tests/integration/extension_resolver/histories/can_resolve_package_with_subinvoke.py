EXPECTED = [
    "wrap://test/package => UriResolverAggregator => package (wrap://test/package)",
    [
        "wrap://test/package => StaticResolver - Miss",
        "wrap://test/package => ExtendableUriResolver => package (wrap://test/package)",
        [
            "wrap://test/package => ResolverExtension (wrap://package/subinvoke-resolver) => package (wrap://test/package)",
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
