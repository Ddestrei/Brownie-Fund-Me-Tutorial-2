from brownie import (
    MockV3Aggregator,
    network,
)
from scripts.helpful_scripts import (
    get_account,
)
from brownie.network import gas_price
from brownie.network.gas.strategies import LinearScalingStrategy

gas_strategy = LinearScalingStrategy("10 gwei", "20 gwei", 1.1)

gas_price(gas_strategy)

DECIMALS = 8
# This is 2,000
INITIAL_VALUE = 200000000000


def deploy_mocks():
    """
    Use this script if you want to deploy mocks to a testnet
    """
    print(f"The active network is {network.show_active()}")
    print("Deploying Mocks...")
    account = get_account()
    MockV3Aggregator.deploy(DECIMALS, INITIAL_VALUE, {
        "from": account,
         "gas_price": gas_strategy})
    print("Mocks Deployed!")


def main():
    deploy_mocks()
