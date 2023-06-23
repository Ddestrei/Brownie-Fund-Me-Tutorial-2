from brownie import network, accounts, exceptions, FundMe, MockV3Aggregator
import pytest
from brownie.network import gas_price
from brownie.network.gas.strategies import LinearScalingStrategy

gas_strategy = LinearScalingStrategy("10 gwei", "20 gwei", 1.1)


DECIMALS = 8
# This is 2,000
INITIAL_VALUE = 200000000000

@pytest.fixture
def mock():
    return MockV3Aggregator.deploy(DECIMALS, INITIAL_VALUE,{"from": accounts[0],"gas_price": gas_strategy})

@pytest.fixture
def fund_me(mock):
    return FundMe.deploy(mock.address,{"from": accounts[0],"gas_price": gas_strategy})

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]

def test_can_fund_and_withdraw(fund_me):
    entrance_fee = fund_me.getEntranceFee() + 100
    tx = fund_me.fund({"from": accounts[0], "value": entrance_fee})
    tx.wait(1)
    assert fund_me.addressToAmountFunded(accounts[0].address) == entrance_fee
    tx2 = fund_me.withdraw({"from": accounts[0]})
    tx2.wait(1)
    assert fund_me.addressToAmountFunded(accounts[0].address) == 0


def test_only_owner_can_withdraw(fund_me):
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("only for local testing")
    bad_actor = accounts.add()
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": bad_actor})