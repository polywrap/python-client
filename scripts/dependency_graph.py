
from collections import Counter, defaultdict
from typing import Generator
import tomlkit
from pathlib import Path
from get_packages import extract_package_paths


def build_dependency_graph():
    dependent_graph: defaultdict[str, set[str]] = defaultdict(set)
    deps_counter: Counter[int] = Counter()

    for package in extract_package_paths():
        package_path = Path(package)
        if package_path.is_dir():
            name = package_path.name
            deps_counter[name] = 0
            with open(package_path.joinpath("pyproject.toml"), "r") as f:
                pyproject = tomlkit.load(f)
                dependencies = pyproject["tool"]["poetry"]["dependencies"]
                for dep in dependencies:
                    if dep.startswith("polywrap-"):
                        dependent_graph[dep].add(name)
                        deps_counter[name] += 1

    return dependent_graph, deps_counter


def topological_order(graph: dict[str, set[str]], counter: dict[str, int]) -> Generator[str, None, None]:
    while counter:
        for dep in list(counter.keys()):
            if counter[dep] == 0:
                yield dep
                for dependent in graph[dep]:
                    counter[dependent] -= 1
                del counter[dep]


def package_build_order() -> Generator[str, None, None]:
    graph, counter = build_dependency_graph()
    return topological_order(graph, counter)


if __name__ == "__main__":
    for package in package_build_order():
        print(package)
