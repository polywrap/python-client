from pathlib import Path
from polywrap_client import PolywrapClient
from polywrap_core import Uri
import pytest


def test_valid_read_file(client: PolywrapClient, ascii_file_path: Path):
    result = client.invoke(
        uri=Uri.from_str("plugin/fs"),
        method="readFile",
        args={"path": str(ascii_file_path)},
    )
    assert result == b"Hello, world!"


def test_invalid_read_file(client: PolywrapClient, temp_dir: Path):
    # Test with an invalid or non-existent file path
    with pytest.raises(Exception) as e:
        client.invoke(
            uri=Uri.from_str("plugin/fs"),
            method="readFile",
            args={"path": str(temp_dir / "non_existent.txt")},
        )

    assert isinstance(e.value.__cause__, FileNotFoundError)
