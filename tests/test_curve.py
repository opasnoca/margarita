def test_alice_is_not_bob(alice, bob):
    assert alice != bob

# test tahat Alice wallet has 0 tokens in tripool cotract
def test_tripool_initialy_unfunded(tripool_lp_token, alice):
    assert tripool_lp_token.balanceOf(alice) == 0

# test that tripool contract is funded with DAI coins from alice
def test_tripool_funded(tripool_lp_token, alice, tripool_funded):
    assert tripool_lp_token.balanceOf(alice) > 0