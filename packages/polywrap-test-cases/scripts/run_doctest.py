# test_all.py
import doctest
from typing import Any
import unittest
import pkgutil
import polywrap_test_cases

def load_tests(loader: Any, tests: Any, ignore: Any) -> Any:
    """Load doctests and return TestSuite object."""
    modules = pkgutil.walk_packages(
        path=polywrap_test_cases.__path__,
        prefix=f"{polywrap_test_cases.__name__}.",
        onerror=lambda x: None,
    )
    tests.addTests(doctest.DocTestSuite(polywrap_test_cases))
    for _, modname, _ in modules:
        try:
            module = __import__(modname, fromlist="dummy")
            tests.addTests(doctest.DocTestSuite(module))
        except (ImportError, ValueError, AttributeError):
            continue
    return tests

if __name__ == "__main__":
    unittest.main()
