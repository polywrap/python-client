import os
from pathlib import Path
from polywrap_client import PolywrapClient
from polywrap_core import Uri
import pytest


def test_rmdir_empty_directory_integration(client: PolywrapClient, temp_dir: Path):
    empty_dir = temp_dir / "empty_dir"
    os.mkdir(empty_dir)

    assert os.path.exists(empty_dir)
    client.invoke(
        uri=Uri.from_str("plugin/fs"),
        method="rmdir",
        args={"path": str(empty_dir)},
    )
    assert not os.path.exists(empty_dir)


def test_rmdir_non_empty_directory_integration(client: PolywrapClient, temp_dir: Path):
    non_empty_dir = temp_dir / "non_empty_dir"
    os.mkdir(non_empty_dir)
    file_path = non_empty_dir / "test_file.txt"
    with open(file_path, "w") as f:
        f.write("Some content")

    assert os.path.exists(non_empty_dir)
    with pytest.raises(Exception) as e:
        client.invoke(
            uri=Uri.from_str("plugin/fs"),
            method="rmdir",
            args={"path": str(non_empty_dir)},
        )

    assert isinstance(e.value.__cause__, OSError)


def test_rmdir_non_existing_directory_integration(
    client: PolywrapClient, temp_dir: Path
):
    non_existing_dir = temp_dir / "non_existing_dir"

    with pytest.raises(Exception) as e:
        client.invoke(
            uri=Uri.from_str("plugin/fs"),
            method="rmdir",
            args={"path": str(non_existing_dir)},
        )

    assert isinstance(e.value.__cause__, FileNotFoundError)
