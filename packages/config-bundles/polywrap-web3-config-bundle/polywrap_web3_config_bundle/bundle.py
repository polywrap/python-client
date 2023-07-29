"""This module contains the configuration for the system bundle."""
from typing import Dict

from polywrap_core import Uri
from polywrap_ethereum_provider import ethereum_provider_plugin
from polywrap_ethereum_provider.connection import Connection
from polywrap_ethereum_provider.connections import Connections
from polywrap_ethereum_provider.networks import KnownNetwork
from polywrap_sys_config_bundle import BundlePackage, sys_bundle
from polywrap_uri_resolvers import ExtendableUriResolver

from .embeds import get_embedded_wrap

ethreum_provider_package = ethereum_provider_plugin(
    Connections(
        connections={
            "mainnet": Connection.from_network(KnownNetwork.mainnet, None),
            "goerli": Connection.from_network(KnownNetwork.goerli, None),
        },
        default_network="mainnet",
    )
)

ipfs_providers = [
    "https://ipfs.wrappers.io",
    "https://ipfs.io",
]


web3_bundle: Dict[str, BundlePackage] = {
    "http": sys_bundle["http"],
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
    "ipfs_http_client": BundlePackage(
        uri=Uri.from_str("embed/ipfs-http-client@1.0.0"),
        package=get_embedded_wrap("ipfs-http-client"),
        implements=[Uri.from_str("ens/wraps.eth:ipfs-http-client@1.0.0")],
        redirects_from=[Uri.from_str("ens/wraps.eth:ipfs-http-client@1.0.0")],
    ),
    "ipfs_resolver": BundlePackage(
        uri=Uri.from_str("embed/sync-ipfs-uri-resolver-ext@1.0.1"),
        package=get_embedded_wrap("ipfs-sync-resolver"),
        implements=[
            Uri.from_str("ens/wraps.eth:sync-ipfs-uri-resolver-ext@1.0.1"),
            *ExtendableUriResolver.DEFAULT_EXT_INTERFACE_URIS,
        ],
        redirects_from=[
            Uri.from_str("ens/wraps.eth:sync-ipfs-uri-resolver-ext@1.0.1"),
        ],
        env={
            "provider": ipfs_providers[0],
            "fallbackProviders": ipfs_providers[1:],
            "retries": {"tryResolveUri": 2, "getFile": 2},
        },
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
