from typing import Any
import pytest
from pathlib import Path


def test_mkdir_new_dir(fs_plugin: Any, temp_dir: Path):
    new_dir_path = temp_dir / "new_dir"
    fs_plugin.mkdir({"path": str(new_dir_path)}, None, None)

    assert new_dir_path.exists() and new_dir_path.is_dir()


def test_mkdir_nested_dir(fs_plugin: Any, temp_dir: Path):
    nested_dir_path = temp_dir / "dir1" / "dir2" / "dir3"
    fs_plugin.mkdir({"path": str(nested_dir_path), "recursive": True}, None, None)

    assert nested_dir_path.exists() and nested_dir_path.is_dir()


def test_mkdir_existing_dir(fs_plugin: Any, temp_dir: Path):
    existing_dir_path = temp_dir / "existing_dir"
    existing_dir_path.mkdir()

    with pytest.raises(FileExistsError):
        fs_plugin.mkdir({"path": str(existing_dir_path)}, None, None)


def test_mkdir_non_recursive(fs_plugin: Any, temp_dir: Path):
    non_recursive_nested_dir_path = temp_dir / "dir1" / "dir2"

    with pytest.raises(FileNotFoundError):
        fs_plugin.mkdir(
            {"path": str(non_recursive_nested_dir_path), "recursive": False}, None, None
        )

    assert not non_recursive_nested_dir_path.exists()
