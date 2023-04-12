import subprocess
import tomlkit


def link_dependencies():
    with open("pyproject.toml", "r") as f:
        pyproject = tomlkit.load(f)

        for dep in list(pyproject["tool"]["poetry"]["dependencies"].keys()):
            if dep.startswith("polywrap-"):
                pyproject["tool"]["poetry"]["dependencies"][dep] = { "path": f"../{dep}", "develop": True }
    
    with open("pyproject.toml", "w") as f:
        tomlkit.dump(pyproject, f)

    subprocess.check_call(["poetry", "update"])


if __name__ == "__main__":
    from pathlib import Path
    from dependency_graph import package_build_order
    from utils import ChangeDir

    root_dir = Path(__file__).parent.parent

    for package in package_build_order():
        with ChangeDir(str(root_dir.joinpath("packages", package))):
            link_dependencies()