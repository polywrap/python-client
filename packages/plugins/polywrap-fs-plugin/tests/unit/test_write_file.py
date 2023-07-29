from typing import Any
from pathlib import Path

def test_write_file_new_file(fs_plugin: Any, temp_dir: Path):
    new_file_path = temp_dir / "new_file.txt"
    content = b"This is a new file."
    fs_plugin.write_file({"path": str(new_file_path), "data": content}, None, None)

    with open(new_file_path, "rb") as f:
        result = f.read()

    assert result == content


def test_write_file_overwrite_existing(fs_plugin: Any, temp_dir: Path):
    existing_file_path = temp_dir / "existing_file.txt"

    with open(existing_file_path, "w") as f:
        f.write("Original content.")

    new_content = b"New content to overwrite the existing one."
    fs_plugin.write_file({"path": str(existing_file_path), "data": new_content}, None, None)

    with open(existing_file_path, "rb") as f:
        result = f.read()

    assert result == new_content
