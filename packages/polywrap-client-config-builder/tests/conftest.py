from polywrap_core import  Uri
from pytest import fixture

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
