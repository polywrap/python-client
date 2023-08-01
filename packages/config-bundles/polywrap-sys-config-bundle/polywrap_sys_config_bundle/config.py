"""This module contains the system configuration for Polywrap Client."""
from polywrap_client_config_builder import BuilderConfig, PolywrapClientConfigBuilder

from .bundle import sys_bundle


def get_sys_config() -> BuilderConfig:
    """Get the system configuration for Polywrap Client."""
    builder = PolywrapClientConfigBuilder()
    for package in sys_bundle.values():
        package.add_to_builder(builder)
    return builder.config


__all__ = ["get_sys_config"]
