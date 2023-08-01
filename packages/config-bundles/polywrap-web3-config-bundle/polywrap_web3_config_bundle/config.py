"""This module contains the system configuration for Polywrap Client."""
from polywrap_client_config_builder import BuilderConfig, PolywrapClientConfigBuilder

from .bundle import web3_bundle


def get_web3_config() -> BuilderConfig:
    """Get the system configuration for Polywrap Client."""
    builder = PolywrapClientConfigBuilder()
    for package in web3_bundle.values():
        package.add_to_builder(builder)
    return builder.config


__all__ = ["get_web3_config"]
