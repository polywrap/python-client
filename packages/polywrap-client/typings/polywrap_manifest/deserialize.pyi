"""
This type stub file was generated by pyright.
"""

from typing import Optional
from polywrap_result import Result
from .manifest import *

"""
This file was automatically generated by scripts/templates/deserialize.py.jinja2.
DO NOT MODIFY IT BY HAND. Instead, modify scripts/templates/deserialize.py.jinja2,
and run python ./scripts/generate.py to regenerate this file.
"""
def deserialize_wrap_manifest(manifest: bytes, options: Optional[DeserializeManifestOptions] = ...) -> Result[AnyWrapManifest]:
    ...

