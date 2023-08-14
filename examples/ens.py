
from polywrap_core import Uri
from polywrap_client import PolywrapClient
from polywrap_client_config_builder import PolywrapClientConfigBuilder
from polywrap_ethereum_provider import ethereum_provider_plugin, Connections, Connection
from polywrap_sys_config_bundle import sys_bundle


if __name__ == "__main__":
    domain = "vitalik.eth"
    ens_uri = Uri.from_str("wrapscan.io/polywrap/ens@1.0.0")

    builder = PolywrapClientConfigBuilder()
    builder.add_bundle(sys_bundle)

    mainnet_connection = Connection.from_node("https://mainnet.infura.io/v3/f1f688077be642c190ac9b28769daecf")

    connections = Connections({
        "mainnet": mainnet_connection,
    }, default_network="mainnet")

    wallet_plugin = ethereum_provider_plugin(connections)

    builder.set_package(Uri.from_str("wrapscan.io/polywrap/ethereum-wallet@1.0"), wallet_plugin)
    config = builder.build()
    client = PolywrapClient(config)

    resolver_address = client.invoke(
        uri=ens_uri,
        method="getResolver",
        args={
            "registryAddress": "0x00000000000C2E074eC69A0dFb2997BA6C7d2e1e",
            "domain": domain
        }
    )

    print(f"Resolver address: {resolver_address}")

    content_hash = client.invoke(
        uri=ens_uri,
        method="getContentHash",
        args={
            "registryAddress": resolver_address,
            "domain": domain
        }
    )

    print(f"Content hash of {domain}: {content_hash}")
