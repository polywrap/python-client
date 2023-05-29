EXPECTED = [
    'wrap://test/not-a-match => UriResolverAggregator => error (Unable to find URI wrap://test/undefined-resolver.\ncode: 28 URI NOT FOUND\nuri: wrap://test/undefined-resolver\nuriResolutionStack: [\n  "wrap://test/undefined-resolver => UriResolverAggregator"\n])',
    [
        'wrap://test/not-a-match => ExtendableUriResolver => error (Unable to find URI wrap://test/undefined-resolver.\ncode: 28 URI NOT FOUND\nuri: wrap://test/undefined-resolver\nuriResolutionStack: [\n  "wrap://test/undefined-resolver => UriResolverAggregator"\n])',
        [
            'wrap://test/not-a-match => ResolverExtension (wrap://test/undefined-resolver) => error (Unable to find URI wrap://test/undefined-resolver.\ncode: 28 URI NOT FOUND\nuri: wrap://test/undefined-resolver\nuriResolutionStack: [\n  "wrap://test/undefined-resolver => UriResolverAggregator"\n])',
            [
                'wrap://test/undefined-resolver => Client.loadWrapper => error (Unable to find URI wrap://test/undefined-resolver.\ncode: 28 URI NOT FOUND\nuri: wrap://test/undefined-resolver\nuriResolutionStack: [\n  "wrap://test/undefined-resolver => UriResolverAggregator"\n])',
                ["wrap://test/undefined-resolver => UriResolverAggregator"],
            ],
        ],
    ],
]
