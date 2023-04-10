"""This module contains the base configure class for the client config builder."""
from ..types import BuilderConfig, ClientConfigBuilder


class BaseConfigure(ClientConfigBuilder):
    """BaseConfigure is the base configure class for the client config builder.

    Attributes:
        config (BuilderConfig): The internal configuration.
    """

    config: BuilderConfig

    def add(self, config: BuilderConfig) -> ClientConfigBuilder:
        """Add the values from the given config to the builder's config."""
        if config.envs:
            self.config.envs.update(config.envs)
        if config.interfaces:
            self.config.interfaces.update(config.interfaces)
        if config.redirects:
            self.config.redirects.update(config.redirects)
        if config.resolvers:
            self.config.resolvers.extend(config.resolvers)
        if config.wrappers:
            self.config.wrappers.update(config.wrappers)
        if config.packages:
            self.config.packages.update(config.packages)
        return self
