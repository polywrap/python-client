import os
from polywrap_test_cases import get_path_to_test_wrappers
import pytest


@pytest.mark.parametrize(
    "wrapper", ["asyncify", "bigint-type", "enum-type", "map-type"]
)
@pytest.mark.parametrize("language", ["as", "rs"])
def test_wrappers_exist(wrapper: str, language: str):
    assert os.path.exists(get_path_to_test_wrappers())
    wrapper_path = os.path.join(get_path_to_test_wrappers(), wrapper, "implementations", language)
    assert os.path.exists(wrapper_path)
    assert os.path.isdir(wrapper_path)
    assert os.path.exists(os.path.join(wrapper_path, "wrap.info"))
    assert os.path.exists(os.path.join(wrapper_path, "wrap.wasm"))
