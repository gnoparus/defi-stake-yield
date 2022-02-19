from scripts.helpful_scripts import (
    get_account,
    fund_with_link,
    get_account,
    get_contract,
)
from brownie import DappToken, TokenFarm, network, config
from web3 import Web3

KEPT_BALANCE = Web3.toWei(1000, "ether")

dict_of_allowed_token = {
    "dapp_token": get_contract("dapp_token"),
    "fau_token": get_contract("fau_token"),
    "weth_token": get_contract("weth_token"),
}


def deploy_dapp_token():
    account = get_account()
    dapp_token = DappToken.deploy(
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )
    return dapp_token


def deploy_token_farm(_dapp_token):
    account = get_account()
    token_farm = TokenFarm.deploy(
        _dapp_token,
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )

    tx = _dapp_token.transfer(
        token_farm.address,
        _dapp_token.totalSupply() - KEPT_BALANCE,
        {"from": account},
    )
    tx.wait(1)
    return token_farm


def add_allowed_tokens(token_farm, dict_of_allowed_token):
    account = get_account()
    for key in dict_of_allowed_token:
        # print(key)
        token_farm.addAllowedToken(dict_of_allowed_token[key])


def main():
    dapp_token = deploy_dapp_token()
    token_farm = deploy_token_farm(dapp_token)
    add_allowed_tokens(token_farm, dict_of_allowed_token=dict_of_allowed_token)
