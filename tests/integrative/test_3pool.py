import pytest
from conftest import load_contract

@pytest.mark.parametrize('i', range(10))
def test_3pool_redeposit(alice, registry, tripool_funded, tripool_lp_token, i):
    # Load Pool for a particular value i offset
    _complement = registry.get_coin_swap_complement(tripool_lp_token, i)
    _pool_addr = registry.find_pool_for_coins(tripool_lp_token, _complement)
    _pool = load_contract(_pool_addr)

    # Approve transfer
    _amout = 1e20
    tripool_lp_token.approve(_pool, _amout, {'from': alice})

    # Make the transfer, require [0, 1e21]
    amounts = [0] * (registry.get_n_coins(_pool)[0])
    _offset = registry.get_coin_indices(_pool, tripool_lp_token, _complement)
    amounts[_offset[0]] = _amout
    _pool.add_liquidity(amounts, 0, {'from': alice})

    # Verify the transfer, by looking at Alice's lp_token balance
    _pool_lq = load_contract(registry.get_lp_token(_pool))
    assert _pool_lq.balanceOf(alice) > 0