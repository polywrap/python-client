import pytest

from pathlib import Path

from polywrap_core import FileReader, UriPackage, UriResolver, Uri
from polywrap_uri_resolvers import FsUriResolver, SimpleFileReader

@pytest.fixture
def file_reader():
    return SimpleFileReader()

@pytest.fixture
def fs_resolver(file_reader: FileReader):
    return FsUriResolver(file_reader=file_reader)


def test_file_resolver(fs_resolver: UriResolver):
    path = Path(__file__).parent / "cases" / "simple"
    uri = Uri.from_str(f"wrap://fs/{path}")

    result = fs_resolver.try_resolve_uri(uri, None, None) # type: ignore

    assert result
    assert isinstance(result, UriPackage)
