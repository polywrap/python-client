import pytest
import tempfile
from pathlib import Path
from polywrap_fs_plugin import FileSystemPlugin


@pytest.fixture
def fs_plugin():
    return FileSystemPlugin(None)

@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir)


@pytest.fixture
def ascii_file_path(temp_dir: Path):
    file_path = temp_dir / "test.txt"
    with open(file_path, "wb") as f:
        f.write("Hello, world!".encode("ascii"))
    return file_path


@pytest.fixture
def ucs2_file_path(temp_dir: Path):
    file_path = temp_dir / "test.txt"
    with open(file_path, "wb") as f:
        f.write("Hello, world!".encode("utf-16"))
    return file_path


@pytest.fixture
def utf16le_file_path(temp_dir: Path):
    file_path = temp_dir / "test.txt"
    with open(file_path, "wb") as f:
        f.write("Hello, world!".encode("utf-16-le"))
    return file_path

