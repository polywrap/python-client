import os
from typing import Any
import pytest
from pathlib import Path

def test_rmdir_empty_directory(fs_plugin: Any, temp_dir: Path):
    empty_dir = temp_dir / "empty_dir"
    os.mkdir(empty_dir)

    assert os.path.exists(empty_dir)
    fs_plugin.rmdir({"path": str(empty_dir)}, None, None)
    assert not os.path.exists(empty_dir)


def test_rmdir_non_empty_directory(fs_plugin: Any, temp_dir: Path):
    non_empty_dir = temp_dir / "non_empty_dir"
    os.mkdir(non_empty_dir)
    file_path = non_empty_dir / "test_file.txt"
    with open(file_path, "w") as f:
        f.write("Some content")

    assert os.path.exists(non_empty_dir)
    with pytest.raises(OSError):
        fs_plugin.rmdir({"path": str(non_empty_dir)}, None, None)


def test_rmdir_non_existing_directory(fs_plugin: Any, temp_dir: Path):
    non_existing_dir = temp_dir / "non_existing_dir"

    with pytest.raises(FileNotFoundError):
        fs_plugin.rmdir({"path": str(non_existing_dir)}, None, None)
