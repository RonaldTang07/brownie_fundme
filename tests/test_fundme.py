from scripts.helperfunctions import getaccount, LOCAL_BLOCKCHAIN_ENVIRONMENT
from scripts.deploy import deploy_fundme
from brownie import network, accounts, exceptions
import pytest


def test_can_fundandwithdraw():
    account = getaccount()
    contract_interact = deploy_fundme()
    entrancefee = contract_interact.getentrancefee()
    tx = contract_interact.addfund({"from": account, "value": entrancefee})
    tx.wait(2)
    assert contract_interact.addresstoamountfunded(
        account.address) == entrancefee
    tx2 = contract_interact.withdraw({"from": account})
    tx2.wait(2)
    assert contract_interact.addresstoamountfunded(account.address) == 0


def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENT:
        pytest.skip("Only for local testing")
    contract_interact = deploy_fundme()
    bad_actor = accounts.add() # add random account
    with pytest.raises(exceptions.VirtualMachineError):
        contract_interact.withdraw({"from": bad_actor})
