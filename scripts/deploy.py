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
    dapp_token = _dapp_token
    token_farm = TokenFarm.deploy(
        _dapp_token,
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )

    ### Transfer most of token to token_farm
    tx = _dapp_token.transfer(
        token_farm.address,
        _dapp_token.totalSupply() - KEPT_BALANCE,
        {"from": account},
    )
    tx.wait(1)

    ## dapp_token, weth_token, fau_token/dai
    weth_token = get_contract("weth_token")
    fau_token = get_contract("fau_token")

    dict_of_allowed_token = {
        dapp_token: get_contract("dai_usd_price_feed"),
        fau_token: get_contract("dai_usd_price_feed"),
        weth_token: get_contract("eth_usd_price_feed"),
    }
    add_allowed_tokens(
        token_farm=token_farm,
        dict_of_allowed_tokens=dict_of_allowed_token,
        account=account,
    )
    return token_farm, dapp_token


def add_allowed_tokens(token_farm, dict_of_allowed_tokens, account):
    for token in dict_of_allowed_tokens:
        add_tx = token_farm.addAllowedToken(token, {"from": account})
        add_tx.wait(1)
        set_tx = token_farm.setPriceFeedContract(token, dict_of_allowed_tokens[token])
        set_tx.wait(1)
    return token_farm


def main():
    dapp_token = deploy_dapp_token()
    token_farm, dapp_token = deploy_token_farm(dapp_token)
