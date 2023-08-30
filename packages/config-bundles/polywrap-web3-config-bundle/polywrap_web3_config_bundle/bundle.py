"""This module contains the configuration for the system bundle."""
from typing import Dict

from polywrap_client_config_builder import BundlePackage
from polywrap_core import Uri
from polywrap_ethereum_wallet import ethereum_wallet_plugin
from polywrap_ethereum_wallet.connection import Connection
from polywrap_ethereum_wallet.connections import Connections
from polywrap_ethereum_wallet.networks import KnownNetwork
from polywrap_sys_config_bundle import sys_bundle
from polywrap_uri_resolvers import ExtendableUriResolver

ethreum_provider_package = ethereum_wallet_plugin(
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
    "http_resolver": sys_bundle["http_resolver"],
    "wrapscan_resolver": sys_bundle["wrapscan_resolver"],
    "ipfs_http_client": sys_bundle["ipfs_http_client"],
    "ipfs_resolver": sys_bundle["ipfs_resolver"],
    "ethreum_provider": BundlePackage(
        uri=Uri.from_str("plugin/ethereum-wallet@1.0"),
        package=ethreum_provider_package,
        implements=[
            Uri.from_str("wrapscan.io/polywrap/ethereum-wallet@1.0"),
        ],
        redirects_from=[
            Uri.from_str("wrapscan.io/polywrap/ethereum-wallet@1.0"),
        ],
    ),
    "ens_text_record_resolver": BundlePackage(
        uri=Uri.from_str("wrap://ipfs/QmdYoDrXPxgjSoWuSWirWYxU5BLtpGVKd3z2GXKhW2VXLh"),
        implements=[
            Uri.from_str("wrapscan.io/polywrap/ens-text-record-uri-resolver@1.0"),
            *ExtendableUriResolver.DEFAULT_EXT_INTERFACE_URIS,
        ],
        redirects_from=[
            Uri.from_str("wrapscan.io/polywrap/ens-text-record-uri-resolver@1.0"),
        ],
        env={"registryAddress": "0x00000000000C2E074eC69A0dFb2997BA6C7d2e1e"},
    ),
    "ens_contenthash_resolver": BundlePackage(
        uri=Uri.from_str("wrapscan.io/polywrap/ens-contenthash-uri-resolver@1.0"),
        implements=[
            *ExtendableUriResolver.DEFAULT_EXT_INTERFACE_URIS,
        ],
    ),
    "ens_ipfs_contenthash_resolver": BundlePackage(
        uri=Uri.from_str("wrapscan.io/polywrap/ens-ipfs-contenthash-uri-resolver@1.0"),
        implements=[
            *ExtendableUriResolver.DEFAULT_EXT_INTERFACE_URIS,
        ],
    ),
}


__all__ = ["web3_bundle"]
