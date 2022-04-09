#!/usr/bin/python3

import pytest
from brownie import Contract
from brownie_tokens import MintableForkToken


@pytest.fixture(scope="function", autouse=True)
def isolate(fn_isolation):
    # perform a chain rewind after completing each test, to ensure proper isolation
    # https://eth-brownie.readthedocs.io/en/v1.10.3/tests-pytest-intro.html#isolation-fixtures
    pass


@pytest.fixture(scope="module")
def margarita(Token, accounts):
    return Token.deploy("Margarita", "MARG", 18, 1e21, {'from': accounts[0]})

# Fixtures are declared by prepending the function with the fixture decorator
# scope "module" declares that every time new module is open this fixture will be rerun
    # There can be diferent scopes of fixtures
    #     function: (default) fixture destroyed at end of test
    #     class: fixture destroyed at last test in class
    #     module: fixture destroyed at last test in module
    #     session: fixture destroyed at end of test session
@pytest.fixture(scope="module")
def alice(accounts):
    return accounts[0]

@pytest.fixture(scope="module")
def bob(accounts):
    return accounts[1]


def load_contract(addr):
    try:
        cont = Contract(addr)
    except ValueError:
        cont = Contract.from_explorer(addr)
    return cont

# fixture that calls Curve registry
@pytest.fixture(scope="module")
def registry():
    return  load_contract("0x90E00ACe148ca3b23Ac1bC8C240C2a7Dd9c2d7f5")

# fixture that references other fixture (calls registry and extracts 0 contract which is DAI,USDC,USDT contract(
@pytest.fixture(scope="module")
def tripool(registry):
    return load_contract(registry.pool_list(0))

# fixture that references from regitry fixture and tripool fixture and extracts lp_token contract
@pytest.fixture(scope="module")
def tripool_lp_token(registry, tripool):
    return load_contract(registry.get_lp_token(tripool))

# fixtrue that will mint some DAI as MIntableForkToken give it to alice and fund the tripool of DAI,USDC,USDT)
@pytest.fixture(scope="module")
def tripool_funded(registry, alice, tripool):
    # creates addres for DAI from treepool contract (coin 0 is DAI coin)
    dai_addr = registry.get_coins(tripool)[0]
    #create DAI token for exploration
    dai = MintableForkToken(dai_addr)
    # create ammount which we wnat ot have
    amount = 1e21
    # aprove fuccion for safty as always
    dai.approve(tripool, amount, {'from': alice})
    dai._mint_for_testing(alice, amount)

    # add liquditiy comand [DAI, USDC, USDT]
    amounts = [amount, 0, 0]
    tripool.add_liquidity(amounts, 0, {'from': alice})
    return tripool
