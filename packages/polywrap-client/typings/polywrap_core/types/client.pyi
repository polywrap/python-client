"""
This type stub file was generated by pyright.
"""

from abc import abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Optional, Union
from polywrap_manifest import AnyWrapManifest, DeserializeManifestOptions
from polywrap_result import Result
from .env import Env
from .invoke import Invoker
from .uri import Uri
from .uri_resolver import IUriResolver
from .uri_resolver_handler import UriResolverHandler

@dataclass(slots=True, kw_only=True)
class ClientConfig:
    envs: Dict[Uri, Env] = ...
    interfaces: Dict[Uri, List[Uri]] = ...
    resolver: IUriResolver


@dataclass(slots=True, kw_only=True)
class GetFileOptions:
    path: str
    encoding: Optional[str] = ...


@dataclass(slots=True, kw_only=True)
class GetManifestOptions(DeserializeManifestOptions):
    ...


class Client(Invoker, UriResolverHandler):
    @abstractmethod
    def get_interfaces(self) -> Dict[Uri, List[Uri]]:
        ...
    
    @abstractmethod
    def get_envs(self) -> Dict[Uri, Env]:
        ...
    
    @abstractmethod
    def get_env_by_uri(self, uri: Uri) -> Union[Env, None]:
        ...
    
    @abstractmethod
    def get_uri_resolver(self) -> IUriResolver:
        ...
    
    @abstractmethod
    async def get_file(self, uri: Uri, options: GetFileOptions) -> Result[Union[bytes, str]]:
        ...
    
    @abstractmethod
    async def get_manifest(self, uri: Uri, options: Optional[GetManifestOptions] = ...) -> Result[AnyWrapManifest]:
        ...
    


