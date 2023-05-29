EXPECTED = [
    "wrap://test/from => UriResolverAggregator => uri (wrap://test/to)",
    [
        "wrap://test/from => StaticResolver - Miss",
        "wrap://test/from => ExtendableUriResolver => uri (wrap://test/to)",
        [
            "wrap://test/from => ResolverExtension (wrap://package/subinvoke-resolver) => uri (wrap://test/to)",
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
    "wrap://test/to => UriResolverAggregator",
    [
        "wrap://test/to => StaticResolver - Miss",
        "wrap://test/to => ExtendableUriResolver",
        [
            "wrap://test/to => ResolverExtension (wrap://package/subinvoke-resolver)",
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
