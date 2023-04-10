"""This module contains the env configure class for the client config builder."""
from typing import Dict, List, Union

from polywrap_core import Env, Uri

from ..types import ClientConfigBuilder


class EnvConfigure(ClientConfigBuilder):
    """Allows configuring the environment variables."""

    def get_env(self, uri: Uri) -> Union[Env, None]:
        """Return the env for the given uri."""
        return self.config.envs.get(uri)

    def get_envs(self) -> Dict[Uri, Env]:
        """Return the envs from the builder's config."""
        return self.config.envs

    def set_env(self, uri: Uri, env: Env) -> ClientConfigBuilder:
        """Set the env by uri in the builder's config, overiding any existing values."""
        self.config.envs[uri] = env
        return self

    def set_envs(self, uri_envs: Dict[Uri, Env]) -> ClientConfigBuilder:
        """Set the envs in the builder's config, overiding any existing values."""
        self.config.envs.update(uri_envs)
        return self

    def add_env(self, uri: Uri, env: Env) -> ClientConfigBuilder:
        """Add an env for the given uri.

        If an Env is already associated with the uri, it is modified.
        """
        if self.config.envs.get(uri):
            for key in self.config.envs[uri]:
                self.config.envs[uri][key] = env[key]
        else:
            self.config.envs[uri] = env
        return self

    def add_envs(self, uri_envs: Dict[Uri, Env]) -> ClientConfigBuilder:
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
