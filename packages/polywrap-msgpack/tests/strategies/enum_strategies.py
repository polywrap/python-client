from enum import IntEnum
from hypothesis import strategies as st


class TestEnum(IntEnum):
    Test0 = 0
    Test1 = 1
    Test2 = 2
    Test3 = 3


def enum_st() -> st.SearchStrategy[IntEnum]:
    """Define a strategy for generating valid `Enum`."""
    return st.sampled_from(list(TestEnum))
