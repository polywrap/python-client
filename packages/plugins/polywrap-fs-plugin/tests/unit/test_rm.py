import os
from typing import Any
import pytest
from pathlib import Path

def test_rm_valid_file(fs_plugin: Any, temp_dir: Path):
    file_path = temp_dir / "test_file.txt"
    with open(file_path, "w") as f:
        f.write("Some content")

    assert os.path.exists(file_path)
    fs_plugin.rm({"path": str(file_path)}, None, None)
    assert not os.path.exists(file_path)


def test_rm_non_existing_file(fs_plugin: Any, temp_dir: Path):
    non_existing_file = temp_dir / "non_existing_file.txt"

    with pytest.raises(FileNotFoundError):
        fs_plugin.rm({"path": str(non_existing_file)}, None, None)


def test_rm_non_existing_dir(fs_plugin: Any, temp_dir: Path):
    non_existing_dir = temp_dir / "non_existing_dir"

    with pytest.raises(FileNotFoundError):
        fs_plugin.rm({"path": str(non_existing_dir)}, None, None)


def test_rm_empty_directory(fs_plugin: Any, temp_dir: Path):
    empty_dir = temp_dir / "empty_dir"
    os.mkdir(empty_dir)

    assert os.path.exists(empty_dir)
    fs_plugin.rm({"path": str(empty_dir)}, None, None)
    assert not os.path.exists(empty_dir)


def test_rm_non_empty_directory_without_recursive(fs_plugin: Any, temp_dir: Path):
    non_empty_dir = temp_dir / "non_empty_dir"
    os.mkdir(non_empty_dir)
    file_path = non_empty_dir / "test_file.txt"
    with open(file_path, "w") as f:
        f.write("Some content")

    assert os.path.exists(non_empty_dir)
    with pytest.raises(OSError):
        fs_plugin.rm({"path": str(non_empty_dir)}, None, None)


def test_rm_non_empty_directory_recursive(fs_plugin: Any, temp_dir: Path):
    non_empty_dir = temp_dir / "non_empty_dir"
    os.mkdir(non_empty_dir)
    file_path = non_empty_dir / "test_file.txt"
    with open(file_path, "w") as f:
        f.write("Some content")

    assert os.path.exists(non_empty_dir)
    fs_plugin.rm({"path": str(non_empty_dir), "recursive": True}, None, None)
    assert not os.path.exists(non_empty_dir)


def test_rm_non_empty_directory_force_no_recursive(fs_plugin: Any, temp_dir: Path):
    non_empty_dir = temp_dir / "non_empty_dir"
    os.mkdir(non_empty_dir)
    file_path = non_empty_dir / "test_file.txt"
    with open(file_path, "w") as f:
        f.write("Some content")

    with pytest.raises(OSError):
        assert os.path.exists(non_empty_dir)
        fs_plugin.rm({"path": str(non_empty_dir), "force": True}, None, None)


def test_rm_non_empty_directory_recursive_and_force(fs_plugin: Any, temp_dir: Path):
    non_empty_dir = temp_dir / "non_empty_dir"
    os.mkdir(non_empty_dir)
    file_path = non_empty_dir / "test_file.txt"
    with open(file_path, "w") as f:
        f.write("Some content")

    assert os.path.exists(non_empty_dir)
    fs_plugin.rm({"path": str(non_empty_dir), "recursive": True, "force": True}, None, None)
    assert not os.path.exists(non_empty_dir)
