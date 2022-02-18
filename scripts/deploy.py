from scripts.helpful_scripts import (
    get_account,
    fund_with_link,
    get_account,
    get_contract,
)
from brownie import DappToken, TokenFarm, network, config
from web3 import Web3

KEPT_BALANCE = Web3.toWei(1000, "ether")


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

def add_allowed_tokens():
    

def main():
    dapp_token = deploy_dapp_token()
    deploy_token_farm(dapp_token)
