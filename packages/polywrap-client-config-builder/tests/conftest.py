from pytest import fixture
from abc import ABC
from typing import Any, Dict, TypeVar, Generic, List
from typing import Generic, Optional, cast
import pytest

from typing import List, Any, Dict, Union
from polywrap_core import Env
from polywrap_core import  Uri
from polywrap_core import IUriResolver, UriPackage, UriWrapper, IWrapPackage
from pytest import fixture
from polywrap_client_config_builder import ClientConfig
from dataclasses import asdict


# polywrap plugins

from polywrap_core import Invoker, InvokeOptions, InvocableResult, GetFileOptions
from polywrap_result import Err, Ok, Result

from polywrap_core import IWrapPackage, Wrapper, GetManifestOptions
from polywrap_manifest import AnyWrapManifest
from polywrap_result import Ok, Result
from polywrap_msgpack import msgpack_decode
from polywrap_core import  Uri

# Variables 

@fixture
def env_varA():
    return { 'color': "yellow", 'size': "large" }

@fixture
def env_varB():
    return { 'color': "red", 'size': "small" }

@fixture
def env_varN():
    return { 'dog': "poodle", 'season': "summer" }

@fixture
def env_varM():
    return { 'dog': "corgi", 'season': "autumn" }

@fixture
def env_varS():
    return { 'vehicle': "scooter"}

# Uris

@fixture
def env_uriX():
    return Uri("wrap://ens/eth.plugin.one/X")

@fixture
def env_uriY():
    return Uri("wrap://ipfs/filecoin.wrapper.two/Y")

@fixture
def env_uriZ():
    return Uri("wrap://pinlist/dev.wrappers.io/Z")




