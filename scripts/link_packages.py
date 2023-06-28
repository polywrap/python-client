import subprocess
import tomlkit


def link_dependencies():
    with open("pyproject.toml", "r") as f:
        pyproject = tomlkit.load(f)

        for dep in list(pyproject["tool"]["poetry"]["dependencies"].keys()):
            if dep.startswith("polywrap-"):
                inline_table = tomlkit.inline_table()
                inline_table.update({"path": f"../{dep}", "develop": True})
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

    for package in package_build_order():
        with ChangeDir(str(root_dir.joinpath("packages", package))):
            link_dependencies()