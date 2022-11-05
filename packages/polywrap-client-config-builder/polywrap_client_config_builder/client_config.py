# Polywrap Python Client - https://polywrap.io
# https://github.com/polywrap/toolchain/blob/origin-0.10-dev/packages/js/client-config-builder/src/ClientConfig.ts


from polywrap_core import Uri, Env
# from polywrap_uri_resolvers import uriresolverlike -> Do this after finishing Envs
from dataclasses import dataclass
from typing import TypeVar, Generic, List

#TUri = TypeVar('TUri', Uri)
@dataclass(slots=True, kw_only=True) 
class ClientConfig:
    """
    This Abstract class is used to configure the polywrap client before it executes a call
    The ClientConfig class is created and modified with the ClientConfigBuilder module
    """
    envs: List[Env]
    #resolver: List[Any] # IUriResolver # -> UriResolverLike