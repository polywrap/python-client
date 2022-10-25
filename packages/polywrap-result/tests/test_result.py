from __future__ import annotations

from typing import Callable

import pytest

from polywrap_result import Err, Ok, Result, UnwrapError

@pytest.fixture
def except1() -> Exception:
    return Exception("error 1")


@pytest.fixture
def except2() -> Exception:
    return Exception("error 1")


def test_ok_factories() -> None:
    instance = Ok(1)
    assert instance._value == 1  # type: ignore
    assert instance.is_ok() is True


def test_err_factories(except1: Exception) -> None:
    instance = Err(except1)
    assert instance._value == except1  # type: ignore
    assert instance.is_err() is True


def test_eq(except1: Exception, except2: Exception) -> None:
    assert Ok(1) == Ok(1)
    assert Err(except1) == Err(except1)
    assert Ok(1) != Err(1)  # type: ignore
    assert Ok(1) != Ok(2)
    assert Err(except1) != Err(except2)
    assert not (Ok(1) != Ok(1))
    assert Ok(1) != "abc"
    assert Ok("0") != Ok(0)


def test_hash(except1: Exception, except2: Exception) -> None:
    assert len({Ok(1), Err(except1), Ok(1), Err(except1)}) == 2
    assert len({Ok(1), Ok(2)}) == 2
    assert len({Ok("a"), Err(except1)}) == 2


def test_repr(except1: Exception) -> None:
    """
    ``repr()`` returns valid code if the wrapped value's ``repr()`` does as well.
    """
    o = Ok(123)
    n = Err(except1)

    assert repr(o) == "Ok(123)"
    assert o == eval(repr(o))

    assert repr(n) == f"Err({repr(except1)})"
    assert n != eval(repr(n))  # error object are different


def test_ok() -> None:
    res = Ok('haha')
    assert res.is_ok() is True
    assert res.is_err() is False
    assert res.value == 'haha'


def test_err() -> None:
    res = Err(':(') # type: ignore
    assert res.is_ok() is False
    assert res.is_err() is True
    assert res.value == ':('


def test_ok_method(except1: Exception) -> None:
    o = Ok('yay')
    n = Err(except1)
    assert o.ok() == 'yay'
    assert n.ok() is None  # type: ignore[func-returns-value]


def test_err_method(except1: Exception) -> None:
    o = Ok('yay')
    n = Err(except1)
    assert o.err() is None  # type: ignore[func-returns-value]
    assert n.err() == except1


def test_no_arg_ok() -> None:
    top_level: Result[None] = Ok()
    assert top_level.is_ok() is True
    assert top_level.ok() is True


def test_expect(except1: Exception) -> None:
    o = Ok('yay')
    n = Err(except1)
    assert o.expect('failure') == 'yay'
    with pytest.raises(UnwrapError):
        n.expect('failure')


def test_expect_err(except1: Exception) -> None:
    o = Ok('yay')
    n = Err(except1)
    assert n.expect_err('hello') == except1
    with pytest.raises(UnwrapError):
        o.expect_err('hello')


def test_unwrap(except1: Exception) -> None:
    o = Ok('yay')
    n = Err(except1)
    assert o.unwrap() == 'yay'
    with pytest.raises(UnwrapError):
        n.unwrap()


def test_unwrap_err(except1: Exception) -> None:
    o = Ok('yay')
    n = Err(except1)
    assert n.unwrap_err() == except1
    with pytest.raises(UnwrapError):
        o.unwrap_err()


def test_unwrap_or(except1: Exception) -> None:
    o = Ok('yay')
    n = Err(except1)
    assert o.unwrap_or('some_default') == 'yay'
    assert n.unwrap_or('another_default') == 'another_default'


def test_unwrap_or_else(except1: Exception, except2: Exception) -> None:
    o = Ok('yay')
    n = Err(except1)
    assert o.unwrap_or_else(lambda x: "nay") == 'yay'
    assert n.unwrap_or_else(lambda x: except2) == except2


def test_unwrap_or_raise(except1: Exception) -> None:
    o = Ok('yay')
    n = Err(except1)
    assert o.unwrap_or_raise(Exception) == 'yay'
    with pytest.raises(Exception) as exc_info:
        n.unwrap_or_raise(Exception)
    assert exc_info.value.args == ('error 1',)


def test_map() -> None:
    o = Ok('yay')
    n = Err('nay')  # type: ignore
    assert o.map(str.upper).ok() == 'YAY'
    assert n.map(str.upper).err() == 'nay'

    num = Ok(3)
    errnum = Err(2)  # type: ignore
    assert num.map(str).ok() == '3'
    assert errnum.map(str).err() == 2


def test_map_or(except1: Exception) -> None:
    o = Ok('yay')
    n = Err(except1)
    assert o.map_or('hay', str.upper) == 'YAY'
    assert n.map_or(except1, str.upper) == except1

    num = Ok(3)
    errnum = Err(except1)
    assert num.map_or('-1', str) == '3'
    assert errnum.map_or('-1', str) == '-1'


def test_map_or_else(except1: Exception) -> None:
    o = Ok('yay')
    n = Err(except1)
    assert o.map_or_else(lambda: 'hay', str.upper) == 'YAY'
    assert n.map_or_else(lambda: 'hay', str.upper) == 'hay'

    num = Ok(3)
    errnum = Err(except1)
    assert num.map_or_else(lambda: '-1', str) == '3'
    assert errnum.map_or_else(lambda: '-1', str) == '-1'


def test_map_err(except1: Exception, except2: Exception) -> None:
    o = Ok('yay')
    n = Err(except1)
    assert o.map_err(lambda x: except2).ok() == 'yay'
    assert n.map_err(lambda x: except2).err() == except2


def test_and_then(except1: Exception) -> None:
    assert Ok(2).and_then(sq).and_then(sq).ok() == 16
    assert Ok(2).and_then(sq).and_then(to_err).err() == 4
    assert Ok(2).and_then(to_err).and_then(sq).err() == 2
    assert Err(except1).and_then(sq).and_then(sq).err() == except1

    assert Ok(2).and_then(sq_lambda).and_then(sq_lambda).ok() == 16
    assert Ok(2).and_then(sq_lambda).and_then(to_err_lambda).err() == 4
    assert Ok(2).and_then(to_err_lambda).and_then(sq_lambda).err() == 2
    assert Err(except1).and_then(sq_lambda).and_then(sq_lambda).err() == except1


def test_or_else(except1: Exception, except2: Exception) -> None:
    assert Ok(2).or_else(lambda x: Err(except2)).or_else(lambda x: Err(except2)).ok() == 2
    assert Ok(2).or_else(lambda x: Err(except2)).or_else(lambda x: Err(except2)).ok() == 2
    assert Err(except1).or_else(lambda x: Ok(1)).or_else(lambda x: Err(except2)).ok() == 1
    assert Err(except1).or_else(lambda x: Err(except2)).or_else(lambda x: Err(except2)).err().args == except1.args # type: ignore


def test_isinstance_result_type(except1: Exception) -> None:
    o = Ok('yay')
    n = Err(except1)
    assert isinstance(o, (Ok, Err))
    assert isinstance(n, (Ok, Err))
    assert not isinstance(1, (Ok, Err))


def test_error_context(except1: Exception) -> None:
    n = Err(except1)
    with pytest.raises(UnwrapError) as exc_info:
        n.unwrap()
    exc = exc_info.value
    assert exc.result is n


def test_slots(except1: Exception) -> None:
    """
    Ok and Err have slots, so assigning arbitrary attributes fails.
    """
    o = Ok('yay')
    n = Err(except1)
    with pytest.raises(AttributeError):
        o.some_arbitrary_attribute = 1  # type: ignore[attr-defined]
    with pytest.raises(AttributeError):
        n.some_arbitrary_attribute = 1  # type: ignore[attr-defined]




def sq(i: int) -> Result[int]:
    return Ok(i**2)


def to_err(i: int) -> Result[int]:
    return Err(i)  # type: ignore


# Lambda versions of the same functions, just for test/type coverage
sq_lambda: Callable[[int], Result[int]] = lambda i: Ok(i * i)
to_err_lambda: Callable[[int], Result[int]] = lambda i: Err(i)  # type: ignore