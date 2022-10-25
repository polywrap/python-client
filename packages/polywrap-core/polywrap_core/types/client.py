from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional, Union

from .env import Env
from .invoke import Invoker
from .uri import Uri
from .uri_resolver import IUriResolver
from .uri_resolver_handler import UriResolverHandler


@dataclass(slots=True, kw_only=True)
class ClientConfig:
    """
    This object is used to configure the polywrap client before it executes a call
    The ClientConfig class is created and modified with the ClientConfigBuilder module
    
    Defined initially here:
    https://github.com/polywrap/toolchain/blob/origin/packages/js/core/src/types/Client.ts
    """
    envs: List[Env] = field(default_factory=list)
    resolver: IUriResolver
    #interfaces: InterfaceImplementations
    #plugins: PluginRegistration
    #redirects: UriRedirect


@dataclass(slots=True, kw_only=True)
class Contextualized:
    context_id: Optional[str] = None


@dataclass(slots=True, kw_only=True)
class GetEnvsOptions(Contextualized):
    pass


@dataclass(slots=True, kw_only=True)
class GetUriResolversOptions(Contextualized):
    pass


@dataclass(slots=True, kw_only=True)
class GetFileOptions(Contextualized):
    path: str
    encoding: Optional[str] = "utf-8"


class Client(Invoker, UriResolverHandler):
    @abstractmethod
    def get_envs(self, options: Optional[GetEnvsOptions] = None) -> List[Env]:
        pass

    @abstractmethod
    def get_env_by_uri(
        self, uri: Uri, options: Optional[GetEnvsOptions] = None
    ) -> Union[Env, None]:
        pass

    @abstractmethod
    def get_uri_resolver(
        self, options: Optional[GetUriResolversOptions] = None
    ) -> List[IUriResolver]:
        pass

    @abstractmethod
    async def get_file(self, uri: Uri, options: GetFileOptions) -> Union[bytes, str]:
        pass
