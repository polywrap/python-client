import os
from urllib import request
from urllib.error import HTTPError

class ChangeDir:
    def __init__(self, new_path: str):
        self.new_path = new_path
        self.saved_path = os.getcwd()

    def __enter__(self):
        os.chdir(self.new_path)

    def __exit__(self, exc_type, exc_value, traceback):
        os.chdir(self.saved_path)


def is_package_published(package: str, version: str):
    url = f"https://pypi.org/pypi/{package}/{version}/json"
    try:
        with request.urlopen(url, timeout=30) as response:
            return response.status == 200
    except (HTTPError, TimeoutError):
        return False
