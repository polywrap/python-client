# pylint: disable=line-too-long
"""This package contains URI resolvers for polywrap-client.

Resolvers
---------
.. csv-table::
    :header: "resolver", "description"

    "WrapperResolver", "Defines a simple statically registered resolver for a wrapper."
    "PackageResolver", "Defines a simple statically registered resolver for a wrap package."
    "RedirectResolver", "Defines a simple resolver to redirect a URI to another URI."
    "StaticResolver", "Defines a simple resolver that allows registering an Uri to redirect or resolve to wrapper or wrap package."
    "UriResolverAggregator", "Defines a resolver that aggregates a list of resolvers."
    "RecursiveResolver", "Defines a resolver that recursively resolves the URI until the result is no longer a URI."
    "ExtendableUriResolver", "Defines a resolver that resolves a uri to a wrapper by using extension wrappers."
    "ResolutionResultCacheResolver", "Defines a resolver that caches the URI resolution result."

.. csv-table::
    :header: "error", "description"

    "UriResolutionError", "Base class for all errors related to URI resolution."
    "InfiniteLoopError", "Raised when an infinite loop is detected while resolving a URI."
    "UriResolverExtensionError", "Base class for all errors related to URI resolver extensions."
    "UriResolverExtensionNotFoundError", "Raised when an extension resolver wrapper could not be found for a URI."
"""
from .errors import *
from .resolvers import *
from .types import *
