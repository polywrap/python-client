"""Publishes all packages in the monorepo to PyPI

Usage:
    python scripts/publish_packages.py
"""
import os
from pathlib import Path
import subprocess
import logging
from time import sleep
import tomlkit
from utils import is_package_published
from color_logger import ColoredLogger

logger = ColoredLogger("PackagePublisher")


def patch_version(version: str):
    with open("pyproject.toml", "r") as f:
        pyproject = tomlkit.load(f)
        pyproject["tool"]["poetry"]["version"] = version

        for dep in pyproject["tool"]["poetry"]["dependencies"]:
            if dep.startswith("polywrap-"):
                pyproject["tool"]["poetry"]["dependencies"][dep] = version
    
    with open("pyproject.toml", "w") as f:
        tomlkit.dump(pyproject, f)

    subprocess.check_call(["poetry", "lock"])
    subprocess.check_call(["poetry", "install", "--no-root"])


def wait_for_package_publish(package: str, version: str) -> None:
    seconds = 0
    increment = 5
    while seconds < 600: # Wait for 10 minutes
        if is_package_published(package, version):
            logger.info(f"Package {package} with version {version} is published")
            break
        sleep(increment)
        seconds += increment
        logger.info(f"Waiting for {package} to be published for {seconds} seconds")
    
    if seconds == 600:
        raise TimeoutError(f"Package {package} with version {version} is not published after 10 minutes")


def publish_package(package: str, version: str) -> None:
    if is_package_published(package, version):
        logger.warning(f"Skip publish: Package {package} with version {version} is already published")
        return
    

    logger.info(f"Patch version for {package} to {version}")
    patch_version(package, version)

    try:
        subprocess.check_call(["poetry", "publish", "--build", "--username", "__token__", "--password", os.environ["POLYWRAP_BUILD_BOT_PYPI_PAT"]])
    except subprocess.CalledProcessError:
        logger.error(f"Failed to publish {package}")

    wait_for_package_publish(package, version)


if __name__ == "__main__":
    from dependency_graph import package_build_order
    from utils import ChangeDir

    root_dir = Path(__file__).parent.parent
    version_file = root_dir.joinpath("VERSION")
    with open(version_file, "r") as f:
        version = f.read().strip()

    for package in package_build_order():
        with ChangeDir(str(root_dir.joinpath("packages", package))):
            publish_package(package, version)