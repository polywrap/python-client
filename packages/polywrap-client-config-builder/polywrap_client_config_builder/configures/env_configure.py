"""This module contains the env configure class for the client config builder."""
from abc import ABC
from typing import Any, Dict, List, Union

from polywrap_core import Uri

from ..types import BuilderConfig, ClientConfigBuilder


class EnvConfigure(ClientConfigBuilder, ABC):
    """Allows configuring the environment variables."""

    config: BuilderConfig

    def get_env(self, uri: Uri) -> Union[Any, None]:
        """Return the env for the given uri."""
        return self.config.envs.get(uri)

    def get_envs(self) -> Dict[Uri, Any]:
        """Return the envs from the builder's config."""
        return self.config.envs

    def set_env(self, uri: Uri, env: Any) -> ClientConfigBuilder:
        """Set the env by uri in the builder's config, overiding any existing values."""
        self.config.envs[uri] = env
        return self

    def set_envs(self, uri_envs: Dict[Uri, Any]) -> ClientConfigBuilder:
        """Set the envs in the builder's config, overiding any existing values."""
        self.config.envs.update(uri_envs)
        return self

    def add_env(self, uri: Uri, env: Any) -> ClientConfigBuilder:
        """Add an env for the given uri.

        If an Any is already associated with the uri, it is modified.
        """
        if self.config.envs.get(uri):
            for key in self.config.envs[uri]:
                self.config.envs[uri][key] = env[key]
        else:
            self.config.envs[uri] = env
        return self

    def add_envs(self, uri_envs: Dict[Uri, Any]) -> ClientConfigBuilder:
        """Add a list of envs to the builder's config."""
        for uri, env in uri_envs.items():
            self.add_env(uri, env)
        return self

    def remove_env(self, uri: Uri) -> ClientConfigBuilder:
        """Remove the env for the given uri."""
        self.config.envs.pop(uri, None)
        return self

    def remove_envs(self, uris: List[Uri]) -> ClientConfigBuilder:
        """Remove the envs for the given uris."""
        for uri in uris:
            self.remove_env(uri)
        return self
