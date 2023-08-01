from typing import Any
import pytest
from pathlib import Path


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
def test_read_file_as_string(
    fs_plugin: Any, ascii_file_path: Path, encoding: str, expected: str
):
    result = fs_plugin.read_file_as_string(
        {"path": str(ascii_file_path), "encoding": encoding}, None, None
    )
    assert result == expected


def test_read_file_as_string_ucs2(fs_plugin: Any, ucs2_file_path: Path):
    # Test with UTF16LE encoding
    result = fs_plugin.read_file_as_string(
        {"path": str(ucs2_file_path), "encoding": "UCS2"}, None, None
    )
    assert result == "Hello, world!"


def test_read_file_as_string_utf16le(fs_plugin: Any, utf16le_file_path: Path):
    # Test with UTF16LE encoding
    result = fs_plugin.read_file_as_string(
        {"path": str(utf16le_file_path), "encoding": "UTF16LE"}, None, None
    )
    assert result == "Hello, world!"


def test_invalid_read_file_as_string(fs_plugin: Any, temp_dir: Path):
    # Test with an invalid or non-existent file path
    with pytest.raises(FileNotFoundError):
        fs_plugin.read_file_as_string(
            {"path": str(temp_dir / "non_existent.txt")}, None, None
        )
