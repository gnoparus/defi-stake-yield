from brownie import network, config, TokenFarm, exceptions
from scripts.helpful_scripts import (
    get_account,
    get_contract,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    INITIAL_PRICE_FEED_VALUE,
)
from scripts.deploy import deploy_token_farm_and_dapp_token
import pytest


def arrange():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing.")
    account = get_account()
    token_farm, dapp_token = deploy_token_farm_and_dapp_token()
    return account, token_farm, dapp_token


def test_set_price_feed_contract():
    account, token_farm, dapp_token = arrange()
    non_owner_account = get_account(1)

    price_feed_address = get_contract("eth_usd_price_feed").address
    token_farm.setPriceFeedContract(
        dapp_token.address, price_feed_address, {"from": account}
    )

    assert token_farm.tokenPriceFeedMapping(dapp_token.address) == price_feed_address

    with pytest.raises(exceptions.VirtualMachineError):
        token_farm.setPriceFeedContract(
            dapp_token.address, price_feed_address, {"from": non_owner_account}
        )


def test_stake_tokens(amount_staked):
    account, token_farm, dapp_token = arrange()
    non_owner_account = get_account(1)

    dapp_token.approve(token_farm.address, amount_staked, {"from": account})
    token_farm.stakeTokens(amount_staked, dapp_token.address, {"from": account})

    assert (
        token_farm.stakingBalance(dapp_token.address, account.address) == amount_staked
    )
    assert token_farm.uniqueTokensStaked(account.address) == 1
    assert token_farm.stakers(0) == account.address
    assert token_farm.uniqueTokensStaked(account.address) == 1

    return token_farm, dapp_token


def test_issue_tokens(amount_staked):
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing.")

    account = get_account()
    token_farm, dapp_token = deploy_token_farm_and_dapp_token()
    print(f"token_farm balance = {dapp_token.balanceOf(token_farm.address):28.0f}")

    starting_balance = dapp_token.balanceOf(account.address)
    print(f"starting_balance   = {starting_balance:28.0f}")
    non_owner_account = get_account(1)

    dapp_token.approve(token_farm.address, amount_staked, {"from": account})
    token_farm.stakeTokens(amount_staked, dapp_token.address, {"from": account})
    print(f"Staked Tokens")

    starting_balance = dapp_token.balanceOf(account.address)
    print(f"starting_balance   = {starting_balance:28.0f}")

    token_farm.issueTokens({"from": account})
    print(f"Issued tokens")

    ending_balance = dapp_token.balanceOf(account.address)
    print(f"ending_balance     = {ending_balance:28.0f}")
    print(f"starting_balance   = {starting_balance:28.0f}")
    print(f"amount_staked      = {amount_staked:28.0f}")
    assert ending_balance == starting_balance + amount_staked


def main():
    test_issue_tokens(3200 * 10**18)
