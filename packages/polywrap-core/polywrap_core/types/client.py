from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional, Union, Dict, Any

from polywrap_manifest import AnyWrapManifest, DeserializeManifestOptions
from polywrap_result import Result

from .env import Env
from .interface_implementation import InterfaceImplementations
from .invoke import Invoker
from .uri import Uri
from .uri_resolver import IUriResolver
from .uri_resolver_handler import UriResolverHandler


@dataclass(slots=True, kw_only=True)
class ClientConfig:
    # TODO  is this a naive solution? the `Any` type should be more specific (str | Uri | int, etc.)
    envs: Dict[Uri, Dict[str, Any]] = field(default_factory=dict) 
    interfaces: List[InterfaceImplementations] = field(default_factory=list)
    resolver: IUriResolver


@dataclass(slots=True, kw_only=True)
class GetEnvsOptions:
    pass


@dataclass(slots=True, kw_only=True)
class GetUriResolversOptions:
    pass


@dataclass(slots=True, kw_only=True)
class GetFileOptions:
    path: str
    encoding: Optional[str] = "utf-8"


@dataclass(slots=True, kw_only=True)
class GetManifestOptions(DeserializeManifestOptions):
    pass


class Client(Invoker, UriResolverHandler):
    @abstractmethod
    def get_interfaces(self) -> List[InterfaceImplementations]:
        pass

    @abstractmethod
    def get_envs(self, options: Optional[GetEnvsOptions] = None) -> Union[Dict[Uri, Dict[str, Any]], None]:
        pass

    @abstractmethod
    def get_env_by_uri(
        self, uri: Uri, options: Optional[GetEnvsOptions] = None
    ) -> Union[Env, Dict[str, Any], None]:
        pass

    @abstractmethod
    def get_uri_resolver(
        self, options: Optional[GetUriResolversOptions] = None
    ) -> IUriResolver:
        pass

    @abstractmethod
    async def get_file(
        self, uri: Uri, options: GetFileOptions
    ) -> Result[Union[bytes, str]]:
        pass

    @abstractmethod
    async def get_manifest(
        self, uri: Uri, options: Optional[GetManifestOptions] = None
    ) -> Result[AnyWrapManifest]:
        pass
