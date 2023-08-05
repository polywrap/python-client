# test_all.py
import doctest
from typing import Any
import unittest
import pkgutil
import polywrap_http_plugin

def load_tests(loader: Any, tests: Any, ignore: Any) -> Any:
    """Load doctests and return TestSuite object."""
    modules = pkgutil.walk_packages(
        path=polywrap_http_plugin.__path__,
        prefix=f"{polywrap_http_plugin.__name__}.",
        onerror=lambda x: None,
    )
    tests.addTests(doctest.DocTestSuite(polywrap_http_plugin))
    for _, modname, _ in modules:
        try:
            module = __import__(modname, fromlist="dummy")
            tests.addTests(doctest.DocTestSuite(module))
        except (ImportError, ValueError, AttributeError):
            continue
    return tests

if __name__ == "__main__":
    unittest.main()
