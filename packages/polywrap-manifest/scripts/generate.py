from dataclasses import dataclass
from pathlib import Path
from typing import List, Set
from urllib.parse import urlparse

from jinja2 import Environment, FileSystemLoader, select_autoescape
import requests
from improved_datamodel_codegen import InputFileType, generate


def to_module_safe(version: str) -> str:
    return version.replace(".", "_")


@dataclass(slots=True, kw_only=True)
class ManifestVersion:
    manifest_version: str
    manifest_module_version: str
    abi_version: str
    abi_module_version: str


@dataclass(slots=True, kw_only=True)
class AbiVersion:
    abi_version: str
    abi_module_version: str

    def __hash__(self) -> int:
        return hash(self.abi_version)


def render_manifest(versions: List[ManifestVersion], abi_versions: Set[AbiVersion], latest: ManifestVersion) -> None:
    template_dir = Path(__file__).parent / "templates"
    env = Environment(loader=FileSystemLoader(str(template_dir)), autoescape=select_autoescape())
    template = env.get_template("manifest.py.jinja2")

    dest_path = Path(__file__).parent.parent / "polywrap_manifest" / "manifest.py"
    with open(dest_path, "w") as f:
        rendered = template.render(versions=versions, abi_versions=list(abi_versions), latest=latest)
        f.write(rendered)

def render_deserialize(versions: List[ManifestVersion]) -> None:
    template_dir = Path(__file__).parent / "templates"
    env = Environment(loader=FileSystemLoader(str(template_dir)), autoescape=select_autoescape())
    template = env.get_template("deserialize.py.jinja2")

    dest_path = Path(__file__).parent.parent / "polywrap_manifest" / "deserialize.py"
    with open(dest_path, "w") as f:
        rendered = template.render(versions=versions)
        f.write(rendered)


def main():
    res = requests.get(
        "https://raw.githubusercontent.com/polywrap/wrap/master/manifest/wrap.info/versions.json"
    )
    versions_list: List[str] = res.json()
    versions: List[ManifestVersion] = []
    abi_versions: Set[AbiVersion] = set()

    for version in versions_list:
        res = requests.get(
            f"https://raw.githubusercontent.com/polywrap/wrap/master/manifest/wrap.info/{version}.json"
        )
        wrap_manifest = res.json()
        abi_url_path: str = wrap_manifest["properties"]["abi"]["$ref"]
        abi_version = abi_url_path.split("/")[-1].replace(".json", "")
        abi_module_version = to_module_safe(abi_version)
        manifest_module_version = to_module_safe(version)

        versions.append(
            ManifestVersion(
                manifest_version=version,
                manifest_module_version=manifest_module_version,
                abi_version=abi_version,
                abi_module_version=abi_module_version,
            )
        )

        abi_versions.add(
            AbiVersion(abi_version=abi_version, abi_module_version=abi_module_version)
        )

        output = (
            Path(__file__).parent.parent
            / "polywrap_manifest"
            / f"wrap_{manifest_module_version}.py"
        )
        url = urlparse(
            f"https://raw.githubusercontent.com/polywrap/wrap/master/manifest/wrap.info/{version}.json"
        )
        generate(
            url,
            class_name="WrapManifest",
            input_file_type=InputFileType.JsonSchema,
            field_constraints=True,
            snake_case_field=True,
            use_schema_description=True,
            output=output,
        )
    
    latest_version: ManifestVersion = versions[-1]

    render_manifest(versions, abi_versions, latest_version)
    render_deserialize(versions)


if __name__ == "__main__":
    main()
