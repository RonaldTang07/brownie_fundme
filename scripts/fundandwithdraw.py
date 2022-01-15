from brownie import fundme
from scripts.helperfunctions import getaccount


def fund():
    fundme_interact = fundme[-1]
    account = getaccount()
    entrancefee = fundme_interact.getentrancefee()
    print(entrancefee)
    fundme_interact.addfund({"from": account, "value": entrancefee})


def withdraw():
    fundme_interact = fundme[-1]
    account = getaccount()
    fundme_interact.withdraw({"from": account})


def main():
    fund()
    withdraw()
