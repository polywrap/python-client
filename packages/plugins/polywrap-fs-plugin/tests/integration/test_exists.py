from pathlib import Path
from polywrap_client import PolywrapClient
from polywrap_core import Uri

def test_exists_valid_file_integration(client: PolywrapClient, ascii_file_path: Path):
    result = client.invoke(
        uri=Uri.from_str("plugin/fs"),
        method="exists",
        args={"path": str(ascii_file_path)},
    )
    assert result == True


def test_exists_valid_dir_integration(client: PolywrapClient, temp_dir: Path):
    result = client.invoke(
        uri=Uri.from_str("plugin/fs"),
        method="exists",
        args={"path": str(temp_dir)},
    )
    assert result == True


def test_exists_nonexistent_path_integration(client: PolywrapClient):
    non_existent_path = Path("nonexistent_path")
    result = client.invoke(
        uri=Uri.from_str("plugin/fs"),
        method="exists",
        args={"path": str(non_existent_path)},
    )
    assert result == False
