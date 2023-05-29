EXPECTED = [
    "wrap://test/not-a-match => UriResolverAggregator",
    [
        "wrap://test/not-a-match => StaticResolver - Miss",
        "wrap://test/not-a-match => ExtendableUriResolver",
        [
            "wrap://test/not-a-match => ResolverExtension (wrap://package/test-resolver)",
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
