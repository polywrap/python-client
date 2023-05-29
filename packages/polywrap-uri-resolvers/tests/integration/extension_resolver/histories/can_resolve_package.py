EXPECTED = [
    "wrap://test/package => UriResolverAggregator => package (wrap://test/package)",
    [
        "wrap://test/package => StaticResolver - Miss",
        "wrap://test/package => ExtendableUriResolver => package (wrap://test/package)",
        [
            "wrap://test/package => ResolverExtension (wrap://package/test-resolver) => package (wrap://test/package)",
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
]
