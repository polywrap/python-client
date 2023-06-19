EXPECTED = [
    "wrap://test/from => UriResolverAggregator => uri (wrap://test/to)",
    [
        "wrap://test/from => Package (wrap://package/test-resolver)",
        "wrap://test/from => ExtendableUriResolver => uri (wrap://test/to)",
        [
            "wrap://test/from => ResolverExtension (wrap://package/test-resolver) => uri (wrap://test/to)",
            [
                "wrap://package/test-resolver => Client.load_wrapper => wrapper (wrap://package/test-resolver)",
                [
                    "wrap://package/test-resolver => UriResolverAggregator => package (wrap://package/test-resolver)",
                    [
                        "wrap://package/test-resolver => Package (wrap://package/test-resolver) => package (wrap://package/test-resolver)"
                    ],
                ],
                "wrap://package/test-resolver => Wrapper.invoke",
            ],
        ],
    ],
    "wrap://test/to => UriResolverAggregator",
    [
        "wrap://test/to => Package (wrap://package/test-resolver)",
        "wrap://test/to => ExtendableUriResolver",
        [
            "wrap://test/to => ResolverExtension (wrap://package/test-resolver)",
            [
                "wrap://package/test-resolver => Client.load_wrapper => wrapper (wrap://package/test-resolver)",
                [
                    "wrap://package/test-resolver => UriResolverAggregator => package (wrap://package/test-resolver)",
                    [
                        "wrap://package/test-resolver => Package (wrap://package/test-resolver) => package (wrap://package/test-resolver)"
                    ],
                ],
                "wrap://package/test-resolver => Wrapper.invoke",
            ],
        ],
    ],
]
