from pathlib import Path
from polywrap_client import PolywrapClient
from polywrap_core import Uri
import pytest


@pytest.mark.parametrize(
    "encoding,expected",
    [
        ("ASCII", "Hello, world!"),
        ("UTF8", "Hello, world!"),
        ("BASE64", "SGVsbG8sIHdvcmxkIQ=="),
        ("BASE64URL", "SGVsbG8sIHdvcmxkIQ"),
        ("LATIN1", "Hello, world!"),
        ("BINARY", "Hello, world!"),
        ("HEX", "48656c6c6f2c20776f726c6421"),
    ],
)
def test_read_file_as_string_integration(
    client: PolywrapClient, ascii_file_path: Path, encoding: str, expected: str
):
    result = client.invoke(
        uri=Uri.from_str("plugin/fs"),
        method="readFileAsString",
        args={"path": str(ascii_file_path), "encoding": encoding},
    )
    assert result == expected


def test_read_file_as_string_ucs2_integration(
    client: PolywrapClient, ucs2_file_path: Path
):
    # Test with UCS2 encoding
    result = client.invoke(
        uri=Uri.from_str("plugin/fs"),
        method="readFileAsString",
        args={"path": str(ucs2_file_path), "encoding": "UCS2"},
    )
    assert result == "Hello, world!"


def test_read_file_as_string_utf16le_integration(
    client: PolywrapClient, utf16le_file_path: Path
):
    # Test with UTF16LE encoding
    result = client.invoke(
        uri=Uri.from_str("plugin/fs"),
        method="readFileAsString",
        args={"path": str(utf16le_file_path), "encoding": "UTF16LE"},
    )
    assert result == "Hello, world!"


def test_invalid_read_file_as_string_integration(
    client: PolywrapClient, temp_dir: Path
):
    # Test with an invalid or non-existent file path
    with pytest.raises(Exception) as e:
        client.invoke(
            uri=Uri.from_str("plugin/fs"),
            method="readFileAsString",
            args={"path": str(temp_dir / "non_existent.txt")},
        )

    assert isinstance(e.value.__cause__, FileNotFoundError)
