from brownie import Contract
from brownie import accounts
# alowes us to create coins out of nothing so we have something to test contract
from brownie_tokens import MintableForkToken

# def main is always run if we start brownie console and type "run('stake')" which is the name of program
def main():
    dai_addr = "0x6b175474e89094c44da98b954eedeac495271d0f"
    usdc_addr = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"
    registry_addr = "0x90E00ACe148ca3b23Ac1bC8C240C2a7Dd9c2d7f5"

    # Amount of coins that we want to transfer
    amount = 100_000 * 10 ** 18
    # Mint token out of thin air with MintableForkToken command so we have something to transfer
    dai = MintableForkToken(dai_addr)
    # Mint "amount" into the account 0 for testing purposes (we use "_mint_for_testing" command for that)
    dai._mint_for_testing(accounts[0], amount)

    # Create registr for registry addres so we can search for poolsi inside of this contract
    registry = Contract(registry_addr)
    # in pool addres we are searching for pool that contains DAI and USDC
    pool_addr = registry.find_pool_for_coins(dai_addr, usdc_addr)
    # pool is contrect in which we deposit our MintableForkToken
    pool = Contract(pool_addr)

    # dai.approve is always run before depositing coins into addres (costs more gas but it is safer)
    dai.approve(pool_addr, amount, {'from': accounts[0]})
    # add DAI into the Contract pool that contains DAI and USDC
    pool.add_liquidity([amount, 0, 0], 0, {'from': accounts[0]})


    # gauges are reward token pool in which we add reword tokens for additional rewards
    gauges = registry.get_gauges(pool_addr)
    # gauge adres is the way how we extract guges addres out of registry
    gauge_addr = gauges[0][0]
    # gauge Contract is tzped so we can interact with it and deposit reward toknes into it
    gauge_contract = Contract(gauge_addr)

    # lp_token is MintableForkTOken created out of thin air for testing purposes
    lp_token = MintableForkToken(gauge_contract.lp_token())
    # lp_token.approve is always run before depositing coins into addres (costs more gas but it is safer)
    lp_token.approve(gauge_addr, amount, {'from': accounts[0]})
    # deposit lp tokens into gauge contract from account 0 who has invested in DAI USDC pool
    gauge_contract.deposit(lp_token.balanceOf(accounts[0]), {'from': accounts[0]})

