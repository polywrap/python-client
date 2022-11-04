# Polywrap Python Client - https://polywrap.io
# https://github.com/polywrap/toolchain/blob/origin-0.10-dev/packages/js/client-config-builder/src/ClientConfig.ts


from polywrap_core import Uri, Env
from polywrap_uri_resolvers import uriresolverlike
from dataclasses import dataclass
from typing import TypeVar, Generic, List

TUri = TypeVar('TUri', Uri, str)

# export interface ClientConfig<TUri extends Uri | string = Uri | string> {


@dataclass(slots=True, kw_only=True) # TODO Check if with or without slots
class ClientConfig(Generic[TUri]):
    """
    This object is used to configure the polywrap client before it executes a call
    The ClientConfig class is created and modified with the ClientConfigBuilder module
    
    Defined initially here:
    https://github.com/polywrap/toolchain/blob/origin/packages/js/core/src/types/Client.ts
    """
    envs: List[Env]
    #resolver: IUriResolver # -> UriResolverLike
    #interfaces: InterfaceImplementations
    #plugins: PluginRegistration
    #redirects: UriRedirect