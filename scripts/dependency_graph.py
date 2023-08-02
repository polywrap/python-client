
from collections import Counter, defaultdict
from typing import Generator
import tomlkit
from pathlib import Path
from get_packages import extract_package_paths


def build_dependency_graph():
    dependent_graph: defaultdict[str, set[str]] = defaultdict(set)
    deps_counter: Counter[int] = Counter()
    name_to_path: dict[str, Path] = {}

    for package in extract_package_paths():
        package_path = Path(package)
        if package_path.is_dir():
            name = package_path.name
            name_to_path[name] = package_path
            deps_counter[name] = 0
            with open(package_path.joinpath("pyproject.toml"), "r") as f:
                pyproject = tomlkit.load(f)
                dependencies = pyproject["tool"]["poetry"]["dependencies"]
                for dep in dependencies:
                    if dep.startswith("polywrap-"):
                        dependent_graph[dep].add(name)
                        deps_counter[name] += 1

    return dependent_graph, deps_counter, name_to_path


def topological_order(graph: dict[str, set[str]], counter: dict[str, int], name_to_path: dict[str, Path]) -> Generator[Path, None, None]:
    while counter:
        for dep in list(counter.keys()):
            if counter[dep] == 0:
                yield name_to_path[dep]
                for dependent in graph[dep]:
                    counter[dependent] -= 1
                del counter[dep]


def package_build_order() -> Generator[Path, None, None]:
    graph, counter, name_to_path = build_dependency_graph()
    return topological_order(graph, counter, name_to_path)


if __name__ == "__main__":
    for package in package_build_order():
        print(package)
