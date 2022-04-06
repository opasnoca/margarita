#!/usr/bin/python3

import pytest


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