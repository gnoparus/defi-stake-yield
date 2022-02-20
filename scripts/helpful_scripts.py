from brownie import (
    network,
    config,
    accounts,
    interface,
    Contract,
    LinkToken,
    MockDAI,
    MockWETH,
    DappToken,
    VRFCoordinatorMock,
    MockV3Aggregator,
)
from web3 import Web3


NON_FORKED_LOCAL_BLOCKCHAIN_ENVIRONMENTS = [
    "development",
    "ganache-local",
    "hardhat",
    "ganache",
]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = NON_FORKED_LOCAL_BLOCKCHAIN_ENVIRONMENTS + [
    "mainnet-fork",
    "mainnet-fork-dev",
    "binance-fork",
    "matic-fork",
]

DECIMALS = 8
INITIAL_VALUE = 3200 * 10**DECIMALS


def get_account(index=None, id=None):

    if index:
        return accounts[index]
    if id:
        return accounts.load(id)

    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        # use generaged fake account
        return accounts[0]

    # use mm account saved in brownie-config
    return accounts.add(config["wallets"]["from_key"])


contract_to_mock = {
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": LinkToken,
    "weth_token": MockWETH,
    "fau_token": MockDAI,
    "dai_usd_price_feed": MockV3Aggregator,
    "eth_usd_price_feed": MockV3Aggregator,
    "dapp_usd_price_feed": MockV3Aggregator,
}


def get_contract(contract_name):
    contract_type = contract_to_mock[contract_name]

    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            deploy_mocks()
        # MockV3Aggregator[-1 ] , VRFCoordinatorMock , LinkToken
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
    return contract


def deploy_mocks(decimals=DECIMALS, initial_value=INITIAL_VALUE):
    print(f"The active network is {network.show_active()}")
    print(f"Deploying mocks...")
    account = get_account()

    link_token = LinkToken.deploy({"from": account})
    print(f"Deployed LinkToken to {link_token.address}")
    vrf_coordinator = VRFCoordinatorMock.deploy(link_token.address, {"from": account})
    print(f"Deployed VRFCoordinatorMock to {vrf_coordinator.address}")
    dai_token = MockDAI.deploy({"from": account})
    print(f"Deployed MockDAI to {dai_token.address}")
    weth_token = MockWETH.deploy({"from": account})
    print(f"Deployed MockWETH to {weth_token.address}")

    eth_usd_pricefeed = MockV3Aggregator.deploy(8, 32000 * 10**10, {"from": account})
    print(f"Deployed MockV3Aggregator eth_usd_pricefeed to {eth_usd_pricefeed.address}")
    dai_usd_pricefeed = MockV3Aggregator.deploy(8, 1 * 10**10, {"from": account})
    print(f"Deployed MockV3Aggregator dai_usd_pricefeed to {dai_usd_pricefeed.address}")
    dapp_usd_pricefeed = MockV3Aggregator.deploy(8, 1 * 10**10, {"from": account})
    print(
        f"Deployed MockV3Aggregator dapp_usd_pricefeed to {dapp_usd_pricefeed.address}"
    )

    print("Deployed mocks!")


def fund_with_link(
    contract_address, account=None, link_token=None, amount=100000000000000000
):  # 0.1 LINK
    account = account if account else get_account()

    ### using mock contract
    link_token = link_token if link_token else get_contract("link_token")
    tx = link_token.transfer(contract_address, amount, {"from": account})

    ### using mock interface
    # link_token_smartcontract = interface.LinkTokenInterface(link_token.address)
    # tx = link_token_smartcontract.transfer(contract_address, amount, {"from": account})

    tx.wait(1)
    print("Fund contract!")
    return tx
