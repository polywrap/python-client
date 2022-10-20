from polywrap_core import Uri 
from dataclasses import dataclass

from polywrap_core.types.env import Env
from typing import List

from polywrap_core.types.uri_resolver import IUriResolver

# from "./bundles" import get_default_client_config

# Replicate this file
# https://github.com/polywrap/toolchain/blob/origin/packages/js/client-config-builder/src/ClientConfigBuilder.ts

def just_a_function():
    return "Yes"

@dataclass(slots=True, kw_only=True)
class ClientConfigBuilder():
    envs: List[Env]
    resolver: IUriResolver
    # plugins:
    # interfaces
    # redirects


    def add(self):
        """
        Appends each property of the supplied config object to the corresponding array of the builder's config.
        """
        pass

    def add_defaults(self):
        """
        Adds the defaultClientConfig object.

        """
        pass

    def build(self):
        """
        Returns a sanitized config object from the builder's config.
        """
        pass