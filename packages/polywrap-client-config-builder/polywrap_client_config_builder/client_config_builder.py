from polywrap_core import Uri, ClientConfig
from dataclasses import dataclass

from polywrap_core.types.env import Env
from typing import List

from polywrap_core.types.uri_resolver import IUriResolver
from polywrap_core.types.wrapper import WrapperCache

# from "./bundles" import get_default_client_config

# Replicate this file
# https://github.com/polywrap/toolchain/blob/origin/packages/js/client-config-builder/src/ClientConfigBuilder.ts

@dataclass(slots=True, kw_only=True)
class ClientConfigBuilder():
    envs: List[Env]
    resolver: IUriResolver
    # plugins:
    # interfaces
    # redirects


def add(self, config: ClientConfigBuilder) -> ClientConfigBuilder:
    """
    Appends each property of the supplied config object to the corresponding array of the builder's config.
    """
    pass

def add_defaults(self, wrapper_cache: WrapperCache=None) -> ClientConfigBuilder:
    """
    Adds the defaultClientConfig object.

    """
    pass

def add_env(self, uri: Uri | str, env ) -> ClientConfigBuilder:
    pass

def remove_env(self, uri: Uri | str ) -> ClientConfigBuilder:
    pass

def build(self):
    """
    Returns a sanitized config object from the builder's config.
    """
    pass