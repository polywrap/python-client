from .generate import *

from pathlib import Path
from os import path

def get_test_path():
    root = Path(__file__).parent
    cases_path = path.join(Path(root).parent.absolute(), "cases", "") 
    print(cases_path)
    return cases_path