import pytest

from polywrap_core.types.uri import Uri


def test_inserts_wrap_scheme_if_not_present():
    uri = Uri.from_str("authority-v2/path.to.thing.root/sub/path")
    assert uri.uri == "wrap://authority-v2/path.to.thing.root/sub/path"
    assert uri.authority == "authority-v2"
    assert uri.path == "path.to.thing.root/sub/path"


def test_fail_non_uri_input():
    with pytest.raises(ValueError):
        Uri.from_str("not a Uri object")


def test_fail_no_authority():
    expected = "The provided URI has an invalid authority or path"
    with pytest.raises(ValueError, match=expected):
        Uri.from_str("wrap://path")


def test_fail_no_path():
    expected = "The provided URI has an invalid path"
    with pytest.raises(ValueError, match=expected):
        Uri.from_str("wrap://authority/")


def test_fail_invalid_scheme():
    expected = r"The provided URI has an invalid scheme \(must be \'wrap\'\)"
    with pytest.raises(ValueError, match=expected):
        Uri.from_str("http://path/something")


def test_fail_empty_string():
    expected = "The provided URI is empty"
    with pytest.raises(ValueError, match=expected):
        Uri.from_str("")


def test_true_if_uri_valid():
    assert Uri.is_canonical_uri("wrap://valid/uri")


def test_false_if_uri_invalid():
    assert not Uri.is_canonical_uri("wrap://.....")
