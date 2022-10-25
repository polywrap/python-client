from __future__ import annotations

from polywrap_result import Err, Ok, Result


def test_pattern_matching_on_ok_type() -> None:
    """
    Pattern matching on ``Ok()`` matches the contained value.
    """
    o: Result[str] = Ok("yay")
    match o:
        case Ok(value):
            reached = True

    assert value == "yay"
    assert reached


def test_pattern_matching_on_err_type() -> None:
    """
    Pattern matching on ``Err()`` matches the contained value.
    """
    n: Result[int] = Err.from_str("nay")
    match n:
        case Err(value):
            reached = True

    assert value.args == ("nay", )
    assert reached