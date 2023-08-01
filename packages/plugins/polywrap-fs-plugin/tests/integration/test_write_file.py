from pathlib import Path
from polywrap_client import PolywrapClient
from polywrap_core import Uri


def test_write_file_new_file_integration(client: PolywrapClient, temp_dir: Path):
    new_file_path = temp_dir / "new_file.txt"
    content = b"This is a new file."
    client.invoke(
        uri=Uri.from_str("plugin/fs"),
        method="writeFile",
        args={"path": str(new_file_path), "data": content},
    )

    with open(new_file_path, "rb") as f:
        result = f.read()

    assert result == content


def test_write_file_overwrite_existing_integration(
    client: PolywrapClient, temp_dir: Path
):
    existing_file_path = temp_dir / "existing_file.txt"

    with open(existing_file_path, "w") as f:
        f.write("Original content.")

    new_content = b"New content to overwrite the existing one."
    client.invoke(
        uri=Uri.from_str("plugin/fs"),
        method="writeFile",
        args={"path": str(existing_file_path), "data": new_content},
    )

    with open(existing_file_path, "rb") as f:
        result = f.read()

    assert result == new_content
