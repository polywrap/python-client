"""This module contains the configuration for the system bundle."""
from typing import Dict

from polywrap_client_config_builder import BundlePackage
from polywrap_core import Uri
from polywrap_ethereum_provider import ethereum_provider_plugin
from polywrap_ethereum_provider.connection import Connection
from polywrap_ethereum_provider.connections import Connections
from polywrap_ethereum_provider.networks import KnownNetwork
from polywrap_sys_config_bundle import sys_bundle
from polywrap_uri_resolvers import ExtendableUriResolver

ethreum_provider_package = ethereum_provider_plugin(
    Connections(
        connections={
            "mainnet": Connection.from_network(KnownNetwork.mainnet, None),
            "goerli": Connection.from_network(KnownNetwork.goerli, None),
        },
        default_network="mainnet",
    )
)

web3_bundle: Dict[str, BundlePackage] = {
    "http": sys_bundle["http"],
    "ipfs_http_client": sys_bundle["ipfs_http_client"],
    "ipfs_resolver": sys_bundle["ipfs_resolver"],
    "ethreum_provider": BundlePackage(
        uri=Uri.from_str("plugin/ethereum-provider@2.0.0"),
        package=ethreum_provider_package,
        implements=[
            Uri.from_str("ens/wraps.eth:ethereum-provider@2.0.0"),
            Uri.from_str("ens/wraps.eth:ethereum-provider@1.1.0"),
        ],
        redirects_from=[
            Uri.from_str("ens/wraps.eth:ethereum-provider@2.0.0"),
            Uri.from_str("ens/wraps.eth:ethereum-provider@1.1.0"),
        ],
    ),
    "ens_text_record_resolver": BundlePackage(
        uri=Uri.from_str("ipfs/QmXcHWtKkfrFmcczdMSXH7udsSyV3UJeoWzkaUqGBm1oYs"),
        implements=[
            Uri.from_str("ens/wraps.eth:ens-text-record-uri-resolver-ext@1.0.1"),
            *ExtendableUriResolver.DEFAULT_EXT_INTERFACE_URIS,
        ],
        redirects_from=[
            Uri.from_str("ens/wraps.eth:ens-text-record-uri-resolver-ext@1.0.1"),
        ],
        env={"registryAddress": "0x00000000000C2E074eC69A0dFb2997BA6C7d2e1e"},
    ),
    "ethereum-wrapper": BundlePackage(
        uri=Uri.from_str("wrap://ipfs/QmPNnnfiQFyzrgJ7pJ2tWze6pLfqGtHDkWooC2xcsdxqSs"),
        redirects_from=[
            Uri.from_str("ipfs/QmS4Z679ZE8WwZSoYB8w9gDSERHAoWG1fX94oqdWpfpDq3")
        ],
    ),
    "ens_resolver": BundlePackage(
        uri=Uri.from_str("ens/wraps.eth:ens-uri-resolver-ext@1.0.1"),
        implements=[
            *ExtendableUriResolver.DEFAULT_EXT_INTERFACE_URIS,
        ],
        env={"registryAddress": "0x00000000000C2E074eC69A0dFb2997BA6C7d2e1e"},
    ),
    "ens_ipfs_contenthash_resolver": BundlePackage(
        uri=Uri.from_str("wrap://ipfs/QmRFqJaAmvkYm7HyTxy61K32ArUDRD6UqtaGZEgvsBfeHW"),
        implements=[
            *ExtendableUriResolver.DEFAULT_EXT_INTERFACE_URIS,
        ],
    ),
}


__all__ = ["web3_bundle"]
