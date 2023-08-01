import pytest
from pathlib import Path
from polywrap_fs_plugin import FileSystemPlugin


def test_valid_read_file(fs_plugin: FileSystemPlugin, ascii_file_path: Path):
    result = fs_plugin.read_file(
        {"path": str(ascii_file_path)}, NotImplemented, None
    )
    assert result == b"Hello, world!"


def test_invalid_read_file(fs_plugin: FileSystemPlugin, temp_dir: Path):
    # Test with an invalid or non-existent file path
    with pytest.raises(FileNotFoundError):
        fs_plugin.read_file(
            {"path": str(temp_dir / "non_existent.txt")},
            NotImplemented,
            None,
        )
