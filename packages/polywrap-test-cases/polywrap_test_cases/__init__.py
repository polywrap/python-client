"""This package contains the utility functions to fetch the wrappers\
    from the wasm-test-harness repo.

Functions
---------

.. csv-table::
    :header: "function", "description"

    "get_path_to_test_wrappers", "Get the path to the test wrappers."
    "fetch_file", "Fetch a file using HTTP."
    "unzip_file", "Unzip a file to a destination."
    "fetch_wrappers", "Fetch the wrappers from the wasm-test-harness repo."
"""
import io
import os
import zipfile
from urllib.error import HTTPError
from urllib.request import urlopen


def get_path_to_test_wrappers() -> str:
    """Get the path to the test wrappers."""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "wrappers"))


def fetch_file(url: str) -> bytes:
    """Fetch a file using HTTP."""
    with urlopen(url) as response:
        if response.status != 200:
            raise HTTPError(
                url, response.status, "Failed to fetch file", response.headers, None
            )
        return response.read()


def unzip_file(file_buffer: bytes, destination: str) -> None:
    """Unzip a file to a destination."""
    with zipfile.ZipFile(io.BytesIO(file_buffer), "r") as zip_ref:
        zip_ref.extractall(destination)


def fetch_wrappers() -> None:
    """Fetch the wrappers from the wasm-test-harness repo."""
    tag = "0.1.0"
    repo_name = "wasm-test-harness"
    url = f"https://github.com/polywrap/{repo_name}/releases/download/{tag}/wrappers"

    buffer = fetch_file(url)
    zip_built_folder = get_path_to_test_wrappers()
    unzip_file(buffer, zip_built_folder)
