"""This module contains the env configure class for the client config builder."""
from typing import Any, Dict, List, Union, cast

from polywrap_core import Uri

from ..types import BuilderConfig, ClientConfigBuilder


class EnvConfigure:
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
        return cast(ClientConfigBuilder, self)

    def set_envs(self, uri_envs: Dict[Uri, Any]) -> ClientConfigBuilder:
        """Set the envs in the builder's config, overiding any existing values."""
        self.config.envs.update(uri_envs)
        return cast(ClientConfigBuilder, self)

    def add_env(self, uri: Uri, env: Any) -> ClientConfigBuilder:
        """Add an env for the given uri.

        If an Any is already associated with the uri, it is modified.
        """
        if old_env := self.config.envs.get(uri):
            new_env = self._merge_envs(old_env, env)
            self.config.envs[uri] = new_env
        else:
            self.config.envs[uri] = env
        return cast(ClientConfigBuilder, self)

    def add_envs(self, uri_envs: Dict[Uri, Any]) -> ClientConfigBuilder:
        """Add a list of envs to the builder's config."""
        for uri, env in uri_envs.items():
            self.add_env(uri, env)
        return cast(ClientConfigBuilder, self)

    def remove_env(self, uri: Uri) -> ClientConfigBuilder:
        """Remove the env for the given uri."""
        self.config.envs.pop(uri, None)
        return cast(ClientConfigBuilder, self)

    def remove_envs(self, uris: List[Uri]) -> ClientConfigBuilder:
        """Remove the envs for the given uris."""
        for uri in uris:
            self.remove_env(uri)
        return cast(ClientConfigBuilder, self)

    @staticmethod
    def _merge_envs(env1: Dict[str, Any], env2: Dict[str, Any]) -> Dict[str, Any]:
        for key, val in env2.items():
            if key not in env1:
                env1[key] = val
                continue

            if isinstance(val, dict):
                old_val = cast(Dict[str, Any], env1[key])
                new_val = cast(Dict[str, Any], val)

                EnvConfigure._merge_envs(old_val, new_val)
            else:
                env1[key] = val
        return env1
