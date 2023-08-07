# pylint: disable=line-too-long
"""This package contains the core types, interfaces, and utilities of polywrap-client.

Core types
----------

.. csv-table::
    :header: "type", "description"

    "Uri", "Defines a wrapper URI and provides utilities for parsing and validating them."
    "Invoker", "Invoker protocol defines the methods for invoking an invocable."
    "Invocable", "Defines Protocol for an Invocable that can be invoked by an invoker."
    "InvokerClient", "InvokerClient protocol defines core set of functionalities for resolving and invoking an Invocable."
    "Wrapper", "Defines the Wrapper protocol that extends the Invocable."
    "WrapPackage", "Defines protocol for representing the package of a wrapper"
    "FileReader", "Defines the FileReader protocol used by UriResolver."
    "Client", "Defines core set of functionalities for interacting with a wrapper."
    "ClientConfig", "Defines Client configuration dataclass."
    "UriResolutionStep", "Represents a single step in the resolution of a uri."
    "UriResolutionContext", "Represents the context of a uri resolution."
    "UriWrapper", "UriWrapper is a dataclass that contains a URI and a wrapper."
    "UriPackage", "UriPackage is a dataclass that contains a URI and a package."
    "UriPackageOrWrapper", "UriPackageOrWrapper is a Union type alias for a URI, a package, or a wrapper."
    "CleanResolutionStep", "Defines a type to represent resolution history in clean human readable format."

Core Errors
-----------

.. csv-table::
    :header: "error", "description"

    "WrapError", "Base error class for all exceptions related to wrappers."
    "WrapAbortError", "Raises when a wrapper aborts execution."
    "WrapInvocationError", "Raises when there is an error invoking a wrapper."
    "WrapGetImplementationsError", "Raises when there is an error getting implementations of an interface."

Utility functions
-----------------

.. csv-table::
    :header: "function", "description"

    "build_clean_uri_history", "Build a clean history of the URI resolution steps."
    "get_env_from_resolution_path", "Get environment variable from URI resolution history."
    "get_implementations", "Get implementations of an interface with its URI."
"""
from .types import *
from .utils import *
