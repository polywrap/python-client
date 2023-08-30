EXPECTED = [
    "wrap://test/not-a-match => UriResolverAggregator - Error: Failed to resolve uri: wrap://test/not-a-match",
    [
        "wrap://test/not-a-match => ExtendableUriResolver - Error: Failed to resolve uri: wrap://test/not-a-match",
        [
            "wrap://test/not-a-match => ResolverExtension (wrap://test/undefined-resolver) - Error: Failed to resolve uri: wrap://test/not-a-match, using extension resolver: (wrap://test/undefined-resolver)",
            [
                "wrap://test/undefined-resolver => Client.load_wrapper - Error: WrapNotFoundError",
                [
                    "wrap://test/undefined-resolver => UriResolverAggregator",
                    ["wrap://test/undefined-resolver => ExtendableUriResolver"],
                ],
            ],
        ],
    ],
]
