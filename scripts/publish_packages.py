"""Publishes all packages in the monorepo to PyPI

Usage:
    python scripts/publish_packages.py
"""
import os
from pathlib import Path
import subprocess
from time import sleep
import tomlkit
from utils import is_package_published
from color_logger import ColoredLogger

logger = ColoredLogger("PackagePublisher")


def patch_version(version: str):
    with open("pyproject.toml", "r") as f:
        pyproject = tomlkit.load(f)
        pyproject["tool"]["poetry"]["version"] = version

        for dep in list(pyproject["tool"]["poetry"]["dependencies"].keys()):
            if dep.startswith("polywrap-"):
                pyproject["tool"]["poetry"]["dependencies"].pop(dep)
                pyproject["tool"]["poetry"]["dependencies"].add(dep, f"^{version}")
    
    with open("pyproject.toml", "w") as f:
        tomlkit.dump(pyproject, f)

    subprocess.check_call(["poetry", "lock", "--no-interaction", "--no-cache"])
    subprocess.check_call(["poetry", "install"])


def patch_version_with_retries(version: str, retries: int = 30):
    for i in range(retries):
        try:
            patch_version(version)
            break
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to patch version for {package} with {i} retries")
            if i == retries - 1:
                raise TimeoutError(f"Failed to patch version for {package} after {retries} retries") from e
            sleep(10)


def wait_for_pypi_publish(package: str, version: str) -> None:
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


def wait_for_poetry_available(package: str, version: str) -> None:
    seconds = 0
    increment = 5
    while seconds < 600: # Wait for 10 minutes
        try:
            pacver = subprocess.check_output(["poetry", "search", f"{package}@{version}", "|", "grep", package], encoding="utf-8")
            if version in pacver:
                logger.info(f"{package} with version {version} is available with poetry.")
                break
        except subprocess.CalledProcessError:
            sleep(increment)
            seconds += increment
            logger.info(f"Waiting for poetry to be available for {seconds} seconds")
    
    if seconds == 600:
        raise TimeoutError(f"Package {package} with version {version} is not available on poetry after 10 minutes")


def publish_package(package: str, version: str) -> None:
    if is_package_published(package, version):
        logger.warning(f"Skip publish: Package {package} with version {version} is already published")
        return

    logger.info(f"Patch version for {package} to {version}")
    patch_version_with_retries(version)

    try:
        subprocess.check_call(["poetry", "publish", "--build", "--username", "__token__", "--password", os.environ["POLYWRAP_BUILD_BOT_PYPI_PAT"]])
    except subprocess.CalledProcessError:
        logger.error(f"Failed to publish {package}")

    wait_for_pypi_publish(package, version)
    wait_for_poetry_available(package, version)


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