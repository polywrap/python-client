from pathlib import Path

import pytest
from polywrap_msgpack import msgpack_decode, msgpack_encode
from pydantic import ValidationError

from polywrap_manifest import (
    DeserializeManifestOptions,
    WrapManifest_0_1,
    deserialize_wrap_manifest,
)


@pytest.fixture
def test_case_dir() -> Path:
    return Path(__file__).parent / "cases"


@pytest.fixture
def msgpack_manifest(test_case_dir: Path) -> bytes:
    with open(test_case_dir / "simple" / "wrap.info", "rb") as f:
        return f.read()


def test_deserialize_without_validate(msgpack_manifest: bytes):
    deserialized_result = deserialize_wrap_manifest(
        msgpack_manifest, DeserializeManifestOptions(no_validate=True)
    )
    assert deserialized_result.is_ok()

    deserialized = deserialized_result.unwrap()
    assert isinstance(deserialized, WrapManifest_0_1)
    assert deserialized.version.value == "0.1"
    assert deserialized.abi.version == "0.1"
    assert deserialized.name == "Simple"


def test_deserialize_with_validate(msgpack_manifest: bytes):
    deserialized_result = deserialize_wrap_manifest(
        msgpack_manifest, DeserializeManifestOptions()
    )
    assert deserialized_result.is_ok()

    deserialized = deserialized_result.unwrap()
    assert isinstance(deserialized, WrapManifest_0_1)
    assert deserialized.version.value == "0.1"
    assert deserialized.abi.version == "0.1"
    assert deserialized.name == "Simple"


def test_invalid_version(msgpack_manifest: bytes):
    decoded = msgpack_decode(msgpack_manifest)
    decoded["version"] = "bad-str"
    manifest: bytes = msgpack_encode(decoded)

    with pytest.raises(ValueError) as e:
        deserialize_wrap_manifest(manifest).unwrap_or_raise()
    assert e.match("'bad-str' is not a valid WrapManifestVersions")


def test_unaccepted_field(msgpack_manifest: bytes):
    decoded = msgpack_decode(msgpack_manifest)
    decoded["invalid_field"] = "not allowed"
    manifest: bytes = msgpack_encode(decoded)

    with pytest.raises(ValidationError) as e:
        deserialize_wrap_manifest(manifest).unwrap_or_raise()
    assert e.match("extra fields not permitted")


def test_invalid_name(msgpack_manifest: bytes):
    decoded = msgpack_decode(msgpack_manifest)
    decoded["name"] = ("foo bar baz $%##$@#$@#$@#$#$",)
    manifest: bytes = msgpack_encode(decoded)

    with pytest.raises(ValidationError) as e:
        deserialize_wrap_manifest(manifest).unwrap_or_raise()

    assert e.match("str type expected")
