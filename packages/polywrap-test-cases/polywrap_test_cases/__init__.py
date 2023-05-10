"""This package contains the utility functions to fetch the wrappers\
    from the wasm-test-harness repo."""
import io
import os
import zipfile
from urllib.request import urlopen
from urllib.error import HTTPError


def get_path_to_test_wrappers() -> str:
    return os.path.join(os.path.dirname(__file__), '..', 'wrappers')


def fetch_from_github(url: str) -> bytes:
    response = urlopen(url)
    if response.status != 200:
        raise HTTPError(url, response.status, "Failed to fetch file", response.headers, None)
    return response.read()


def unzip_file(file_buffer: bytes, destination: str) -> None:
    with zipfile.ZipFile(io.BytesIO(file_buffer), 'r') as zip_ref:
        zip_ref.extractall(destination)


def fetch_wrappers() -> None:
    tag = "0.1.0"
    repo_name = "wasm-test-harness"
    url = f"https://github.com/polywrap/{repo_name}/releases/download/{tag}/wrappers"

    buffer = fetch_from_github(url)
    zip_built_folder = get_path_to_test_wrappers()
    unzip_file(buffer, zip_built_folder)
