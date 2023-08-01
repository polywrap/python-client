import os
from pathlib import Path
from polywrap_client import PolywrapClient
from polywrap_core import Uri
import pytest


def test_rm_valid_file_integration(client: PolywrapClient, temp_dir: Path):
    file_path = temp_dir / "test_file.txt"
    with open(file_path, "w") as f:
        f.write("Some content")

    assert os.path.exists(file_path)
    client.invoke(
        uri=Uri.from_str("plugin/fs"), method="rm", args={"path": str(file_path)}
    )
    assert not os.path.exists(file_path)


def test_rm_non_existing_file_integration(client: PolywrapClient, temp_dir: Path):
    non_existing_file = temp_dir / "non_existing_file.txt"

    with pytest.raises(Exception) as e:
        client.invoke(
            uri=Uri.from_str("plugin/fs"),
            method="rm",
            args={"path": str(non_existing_file)},
        )

    assert isinstance(e.value.__cause__, FileNotFoundError)


def test_rm_non_existing_dir_integration(client: PolywrapClient, temp_dir: Path):
    non_existing_dir = temp_dir / "non_existing_dir"

    with pytest.raises(Exception) as e:
        client.invoke(
            uri=Uri.from_str("plugin/fs"),
            method="rm",
            args={"path": str(non_existing_dir)},
        )

    assert isinstance(e.value.__cause__, FileNotFoundError)


def test_rm_empty_directory_integration(client: PolywrapClient, temp_dir: Path):
    empty_dir = temp_dir / "empty_dir"
    os.mkdir(empty_dir)

    assert os.path.exists(empty_dir)
    client.invoke(
        uri=Uri.from_str("plugin/fs"),
        method="rm",
        args={"path": str(empty_dir)},
    )
    assert not os.path.exists(empty_dir)


def test_rm_non_empty_directory_without_recursive_integration(
    client: PolywrapClient, temp_dir: Path
):
    non_empty_dir = temp_dir / "non_empty_dir"
    os.mkdir(non_empty_dir)
    file_path = non_empty_dir / "test_file.txt"
    with open(file_path, "w") as f:
        f.write("Some content")

    assert os.path.exists(non_empty_dir)
    with pytest.raises(Exception) as e:
        client.invoke(
            uri=Uri.from_str("plugin/fs"),
            method="rm",
            args={"path": str(non_empty_dir)},
        )

    assert isinstance(e.value.__cause__, OSError)


def test_rm_non_empty_directory_recursive_integration(
    client: PolywrapClient, temp_dir: Path
):
    non_empty_dir = temp_dir / "non_empty_dir"
    os.mkdir(non_empty_dir)
    file_path = non_empty_dir / "test_file.txt"
    with open(file_path, "w") as f:
        f.write("Some content")

    assert os.path.exists(non_empty_dir)
    client.invoke(
        uri=Uri.from_str("plugin/fs"),
        method="rm",
        args={"path": str(non_empty_dir), "recursive": True},
    )
    assert not os.path.exists(non_empty_dir)


def test_rm_non_empty_directory_force_no_recursive_integration(
    client: PolywrapClient, temp_dir: Path
):
    non_empty_dir = temp_dir / "non_empty_dir"
    os.mkdir(non_empty_dir)
    file_path = non_empty_dir / "test_file.txt"
    with open(file_path, "w") as f:
        f.write("Some content")

    with pytest.raises(Exception) as e:
        assert os.path.exists(non_empty_dir)
        client.invoke(
            uri=Uri.from_str("plugin/fs"),
            method="rm",
            args={"path": str(non_empty_dir), "force": True},
        )

    assert isinstance(e.value.__cause__, OSError)


def test_rm_non_empty_directory_recursive_and_force_integration(
    client: PolywrapClient, temp_dir: Path
):
    non_empty_dir = temp_dir / "non_empty_dir"
    os.mkdir(non_empty_dir)
    file_path = non_empty_dir / "test_file.txt"
    with open(file_path, "w") as f:
        f.write("Some content")

    assert os.path.exists(non_empty_dir)
    client.invoke(
        uri=Uri.from_str("plugin/fs"),
        method="rm",
        args={"path": str(non_empty_dir), "recursive": True, "force": True},
    )
    assert not os.path.exists(non_empty_dir)
