EXPECTED = [
    "wrap://test/not-a-match => UriResolverAggregator",
    [
        "wrap://test/not-a-match => Static - Miss",
        "wrap://test/not-a-match => ExtendableUriResolver",
        [
            "wrap://test/not-a-match => ResolverExtension (wrap://package/test-subinvoke-resolver)",
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
