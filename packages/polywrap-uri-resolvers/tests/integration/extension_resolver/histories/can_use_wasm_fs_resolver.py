import os
from polywrap_core import Uri
from polywrap_test_cases import get_path_to_test_wrappers


source_uri = Uri(
    "fs",
    os.path.join(get_path_to_test_wrappers(), "asyncify", "implementations", "as"),
)

EXPECTED = [
    f"{source_uri} => UriResolverAggregator",
    [
        f"{source_uri} => Package (wrap://package/test-fs-resolver)",
        f"{source_uri} => ExtendableUriResolver",
        [
            f"{source_uri} => ResolverExtension (wrap://package/test-fs-resolver)",
            [
                "wrap://package/test-fs-resolver => Client.load_wrapper => wrapper (wrap://package/test-fs-resolver)",
                [
                    "wrap://package/test-fs-resolver => UriResolverAggregator => package (wrap://package/test-fs-resolver)",
                    [
                        "wrap://package/test-fs-resolver => Package (wrap://package/test-fs-resolver) => package (wrap://package/test-fs-resolver)"
                    ],
                ],
                "wrap://package/test-fs-resolver => Wrapper.invoke",
            ],
        ],
    ],
]
