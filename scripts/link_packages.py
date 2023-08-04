import os
import subprocess
from typing import Dict
import tomlkit
from get_packages import extract_package_paths
from pathlib import Path


def link_dependencies(packages: Dict[str, str]):
    with open("pyproject.toml", "r") as f:
        pyproject = tomlkit.load(f)
        curdir = Path.cwd().absolute()

        for dep in list(pyproject["tool"]["poetry"]["dependencies"].keys()):
            if dep.startswith("polywrap-"):
                inline_table = tomlkit.inline_table()
                inline_table.update({"path": os.path.relpath(packages[dep], curdir), "develop": True})
                pyproject["tool"]["poetry"]["dependencies"].pop(dep)
                pyproject["tool"]["poetry"]["dependencies"].add(dep, inline_table)
    
    with open("pyproject.toml", "w") as f:
        tomlkit.dump(pyproject, f)

    subprocess.check_call(["poetry", "lock", "--no-interaction", "--no-cache"])
    subprocess.check_call(["poetry", "install"])


if __name__ == "__main__":
    from pathlib import Path
    from dependency_graph import package_build_order
    from utils import ChangeDir

    root_dir = Path(__file__).parent.parent

    package_paths = map(Path, extract_package_paths())
    packages = {path.name: str(path.absolute()) for path in package_paths}

    for package_dir in package_build_order():
        with ChangeDir(str(package_dir)):
            link_dependencies(packages)
