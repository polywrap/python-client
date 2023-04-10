from polywrap_core import Uri
from polywrap_client_config_builder import PolywrapClientConfigBuilder


def test_sanity():
    config = (
        PolywrapClientConfigBuilder()
        .add_env(Uri.from_str("ens/hello.eth"), {"hello": "world"})
        .build()
    )

    assert config.envs[Uri.from_str("ens/hello.eth")]["hello"] == "world"
