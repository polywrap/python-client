EXPECTED = [
    "wrap://test/package => UriResolverAggregator => package (wrap://test/package)",
    [
        "wrap://test/package => Static - Miss",
        "wrap://test/package => ExtendableUriResolver => package (wrap://test/package)",
        [
            "wrap://test/package => ResolverExtension (wrap://package/test-subinvoke-resolver) => package (wrap://test/package)",
            [
                "wrap://package/test-subinvoke-resolver => Client.load_wrapper => wrapper (wrap://package/test-subinvoke-resolver)",
                [
                    "wrap://package/test-subinvoke-resolver => UriResolverAggregator => package (wrap://package/test-subinvoke-resolver)",
                    [
                        "wrap://package/test-subinvoke-resolver => Static - Package => package (wrap://package/test-subinvoke-resolver)"
                    ],
                ],
                "wrap://package/test-subinvoke-resolver => Wrapper.invoke",
                [
                    "wrap://package/test-resolver => Client.load_wrapper => wrapper (wrap://package/test-resolver)",
                    [
                        "wrap://package/test-resolver => UriResolverAggregator => package (wrap://package/test-resolver)",
                        [
                            "wrap://package/test-resolver => Static - Package => package (wrap://package/test-resolver)"
                        ],
                    ],
                    "wrap://package/test-resolver => Wrapper.invoke",
                ],
            ],
        ],
    ],
]
